#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2018 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from hashlib import md5

from django.utils import timezone
from django.urls import re_path
from django.shortcuts import HttpResponse
from django.db import Error
from django.http import Http404
from django.conf import settings

from basic import models


allow_ips = {
    '136.243.38.147',
    '136.243.38.149',
    '136.243.38.150',
    '136.243.38.151',
    '136.243.38.189',
    '88.198.88.98'
}


required_params = {
    'MERCHANT_ID',
    'AMOUNT',
    'intid',
    'MERCHANT_ORDER_ID',
    'CUR_ID',
    'SIGN',
    'us_item'
}


def payment(request):
    ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if ip is None:
        ip = request.META.get('REMOTE_ADDR')

    if ip not in allow_ips:
        raise Http404()

    if any(required_param not in request.GET for required_param in required_params):
        return HttpResponse('Invalid request')

    data = request.GET.copy()
    key = settings.PAYMENT['secret_key2']
    account = data.get('MERCHANT_ORDER_ID')

    try:
        item_id = int(data.get('us_item'))
        order_sum = int(data.get('AMOUNT'))
        payment_id = int(data.get('intid'))
    except ValueError:
        return HttpResponse('Invalid parameters')

    sign_string = ':'.join((data.get('MERCHANT_ID'), data.get('AMOUNT'), key, account))
    sign = md5(sign_string.encode('utf-8')).hexdigest()

    if data.get('SIGN') != sign:
        return HttpResponse('Incorrect digital signature')

    if data.get('MERCHANT_ID') != settings.PAYMENT['public_key']:
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

            return HttpResponse('YES')
        except Error:
            return HttpResponse('Unable to create task database')

    else:
        return HttpResponse('Payment has already been paid')


urlpatterns = [
    re_path(r'^$', payment),
]
