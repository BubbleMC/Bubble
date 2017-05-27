#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from __future__ import unicode_literals

import hashlib
from datetime import datetime

from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import Error
from django.http import Http404
from django.conf import settings

import basic.models


allowIp = {
    '136.243.38.147',
    '136.243.38.149',
    '136.243.38.150',
    '136.243.38.151',
    '136.243.38.189',
    '88.198.88.98',
    '127.0.0.1'
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
    if ip not in allowIp:
        raise Http404()

    for getParameter in getParameters:
        if getParameter not in request.GET:
            return HttpResponse('Invalid request')

    data = request.GET.copy()
    key = settings.PAYMENT['secretKey2']
    account = data.get('MERCHANT_ORDER_ID')

    try:
        itemId = int(data.get('us_item'))
        orderSum = int(data.get('AMOUNT'))
        paymentId = int(data.get('intid'))
    except ValueError:
        return HttpResponse('Invalid parameters')

    signString = data.get('MERCHANT_ID') + ':' + data.get('AMOUNT') + ':' + key + ':' + account
    sign = hashlib.md5(signString).hexdigest()

    if data.get('SIGN') != sign:
        return HttpResponse('Incorrect digital signature')

    if data.get('MERCHANT_ID') != settings.PAYMENT['publicKey']:
        return HttpResponse('Invalid checkout id')

    try:
        item = basic.models.Item.objects.get(id=itemId)
    except ObjectDoesNotExist:
        return HttpResponse('Invalid purchase subject')

    price = item.item_price

    if orderSum != price:
        return HttpResponse('Invalid payment amount')

    try:
        basic.models.Payment.objects.get(payment_number=paymentId)
    except ObjectDoesNotExist:
        try:
            p = basic.models.Payment(payment_number=paymentId,
                                     payment_account=account,
                                     payment_item=item,
                                     payment_status=1,
                                     payment_dateComplete=datetime.now())
            p.save()
        except Error:
            return HttpResponse('Unable to create payment database')

        try:
            cmd = item.item_cmd.format(account=account)
            task = basic.models.Task(task_cmd=cmd, task_payment=p)
            task.save()
        except Error:
            return HttpResponse('Unable to create task database')

        return HttpResponse('YES')
    else:
        return HttpResponse('Payment has already been paid')


urlpatterns = [
    url(r'^$', payment),
]

