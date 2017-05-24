#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from __future__ import unicode_literals

import hashlib
import base64
import urlparse
from httplib import ACCEPTED

from django.conf.urls import url
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import Error
from django.conf import settings

import basic.models


allowIp = {
    '151.80.190.97',
    '151.80.190.98',
    '151.80.190.99',
    '151.80.190.100',
    '151.80.190.101',
    '151.80.190.102',
    '151.80.190.103',
    '151.80.190.104',
    '127.0.0.1'    #debug
}


getParameters = {
    'ik_co_id',
    'ik_am',
    'ik_cur',
    'ik_x_account'
    'ik_x_item',
    'ik_inv_id',
    'ik_inv_st',
    'ik_inv_crt',
    'ik_inv_prc',
    'ik_sign'
}


def payment(request):
    ip = request.META.get('REMOTE_ADDR')
    if ip not in allowIp:
        raise Http404()

    for getParameter in getParameters:
        if getParameter not in request.GET:
            return HttpResponse('Invalid request', status=ACCEPTED)

    data = request.GET.copy()
    account = data.get('ik_x_account')
    key = settings.PAYMENT['secretKey']

    try:
        orderSum = int(data.get('ik_am'))
        itemId = int(data.get('ik_x_item'))
        paymentId = int(data.get('ik_inv_id'))
    except ValueError:
        return HttpResponse('Invalid parameters', status=ACCEPTED)

    queryString = request.META.get('QUERY_STRING')
    params = urlparse.parse_qsl(queryString)
    params.sort()

    signString = ''
    for param in params:
        if param[0] != 'ik_sign':
            signString += param[1] + ':'
    signString += key
    sign = base64.b64encode(hashlib.md5(signString.encode('utf-8')).digest())

    if data.get('ik_sign') != sign:
        return HttpResponse('Incorrect digital signature', status=ACCEPTED)

    if data.get('ik_inv_st') != 'success':
        return HttpResponse('Invalid payment status', status=ACCEPTED)

    if data.get('ik_co_id') != settings.PAYMENT['publicId']:
        return HttpResponse('Invalid checkout id', status=ACCEPTED)

    try:
        item = basic.models.Item.objects.get(id=itemId)
    except ObjectDoesNotExist:
        return HttpResponse('Invalid purchase subject', status=ACCEPTED)

    price = item.item_price

    if orderSum != price:
        return HttpResponse('Invalid payment amount', status=ACCEPTED)

    try:
        p = basic.models.Payment(payment_number=paymentId,
                                 payment_account=account,
                                 payment_item=item,
                                 payment_status=1,
                                 payment_dateCreate=data.get('ik_inv_crt'),
                                 payment_dateComplete=data.get('ik_inv_prc'))
        p.save()
    except Error:
        return HttpResponse('Unable to create payment database', status=ACCEPTED)

    try:
        cmd = item.item_cmd.format(account=account)
        task = basic.models.Task(task_cmd=cmd, task_payment=p)
        task.save()
    except Error:
        return HttpResponse('Unable to create task database', status=ACCEPTED)

    return HttpResponse()


urlpatterns = [
    url(r'^$', payment),
]
