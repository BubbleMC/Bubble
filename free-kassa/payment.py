#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2018 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
import hashlib

from django.utils import timezone
from django.urls import re_path
from django.shortcuts import HttpResponse
from django.db import Error
from django.http import Http404
from django.conf import settings

from basic import models


allowIps = {
    '136.243.38.147',
    '136.243.38.149',
    '136.243.38.150',
    '136.243.38.151',
    '136.243.38.189',
    '88.198.88.98'
}


getParameters = {
    'MERCHANT_ID',
    'AMOUNT',
    'intid',
    'MERCHANT_ORDER_ID',
    'CUR_ID',
    'SIGN',
    'us_item'
}


def payment(request):
    ip = request.META.get('REMOTE_ADDR')
    if ip not in allowIps:
        raise Http404()

    for getParameter in getParameters:
        if getParameter not in request.GET:
            return HttpResponse('Invalid request')

    data = request.GET.copy()
    key = settings.PAYMENT['secretKey2']
    account = data.get('MERCHANT_ORDER_ID')

    try:
        item_id = int(data.get('us_item'))
        order_sum = int(data.get('AMOUNT'))
        payment_id = int(data.get('intid'))
    except ValueError:
        return HttpResponse('Invalid parameters')

    sign_string = data.get('MERCHANT_ID') + ':' + data.get('AMOUNT') + ':' + key + ':' + account
    sign = hashlib.md5(sign_string).hexdigest()

    if data.get('SIGN') != sign:
        return HttpResponse('Incorrect digital signature')

    if data.get('MERCHANT_ID') != settings.PAYMENT['publicKey']:
        return HttpResponse('Invalid checkout id')

    try:
        item = models.Item.objects.get(id=item_id)
    except models.Item.DoesNotExist:
        return HttpResponse('Invalid purchase subject')

    price = item.item_price

    if order_sum != price:
        return HttpResponse('Invalid payment amount')

    try:
        payment = models.Payment.objects.get(payment_number=payment_id)
    except models.Payment.DoesNotExist:
        try:
            payment = models.Payment(
                payment_number=payment_id,
                payment_account=account,
                payment_item=item,
                payment_status=1,
                payment_dateComplete=timezone.now()
            )
            payment.save()
        except Error:
            return HttpResponse('Unable to create payment database')

        try:
            cmd = item.item_cmd.format(account=account)

            task = models.Task(
                task_cmd=cmd,
                task_payment=payment
            )
            task.save()
        except Error:
            return HttpResponse('Unable to create task database')

        return HttpResponse('YES')
    else:
        return HttpResponse('Payment has already been paid')


urlpatterns = [
    re_path(r'^$', payment),
]
