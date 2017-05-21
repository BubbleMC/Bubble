#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from __future__ import unicode_literals

import hashlib
import urlparse
import re
from datetime import datetime

from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.db import Error
from django.http import Http404, JsonResponse
from django.conf import settings

import basic.models


allowIP = {
    '31.186.100.49',
    '178.132.203.105',
    '52.29.152.23',
    '52.19.56.234',
    '127.0.0.1'
}


def payment(request):
    ip = request.META.get('REMOTE_ADDR')
    if ip not in allowIP:
        raise Http404()

    data = request.GET.copy()
    method = data.get('method')
    itemId = re.findall(r'(?<=-_-)(.*)', data.get('params[account]'))
    account = re.findall(r'(.*)(?=-_-)', data.get('params[account]'))
    key = settings.PAYMENT['secretKey']
    currency = settings.PAYMENT['currency']

    queryString = request.META.get('QUERY_STRING')
    params = urlparse.parse_qsl(queryString)
    params.sort()

    signString = ''
    for param in params:
        if (param[0] != 'params[sign]') and (param[0] != 'params[signature]'):
            signString += param[1] + '{up}'
    signString += key
    sign = hashlib.sha256(signString.encode('utf-8')).hexdigest()

    if data.get('params[sign]') != sign:
        return JsonResponse({'error': {'message': 'Incorrect digital signature'}})

    if method == 'check':
        try:
            p = basic.models.Payment.objects.get(payment_number=data.get('params[unitpayId]'))
        except ObjectDoesNotExist:
            try:
                item = basic.models.Item.objects.get(id=itemId)
            except ObjectDoesNotExist:
                return JsonResponse({'error': {'message': 'Invalid purchase subject'}})

            price = item.item_price

            if price != data.get('params[orderSum]'):
                return JsonResponse({'error': {'message': 'Invalid payment amount'}})
            if currency != data.get('params[orderCurrency]'):
                return JsonResponse({'error': {'message': 'Invalid payment currency'}})

            try:
                p = basic.models.Payment(payment_number=data.get('params[unitpayId]'),
                                         payment_account=account,
                                         payment_item=item)
                p.save()
            except Error:
                return JsonResponse({'error': {'message': 'Unable to create payment database'}})

            JsonResponse({'result': {'message': 'CHECK is successful'}})
        else:
            return JsonResponse({'result': {'message': 'Payment already exists'}})

        return JsonResponse({'result': {'message': 'CHECK is successful'}})

    if method == 'pay':
        try:
            p = basic.models.Payment.obcjects.get(payment_number=data.get('params[unitpayId]'))
        except ObjectDoesNotExist:
            return JsonResponse({'result': {'message': 'Payment not found'}})

        if p.payment_status == 1:
            return JsonResponse({'result': {'message': 'Payment has already been paid'}})

        try:
            p.payment_status = 1
            p.payment_dateComplete = datetime.now()
            p.save()
        except Error:
            return JsonResponse({'result': {'message': 'Unable to confirm payment database'}})

        try:
            item = basic.models.Item.objects.get(id=itemId)
            cmd = item.item_cmd.format(account)
            task = basic.models.Task(task_cmd=cmd, task_payment=p)
            task.save()
        except ObjectDoesNotExist:
            return JsonResponse({'result': {'message': 'Invalid purchase subject'}})
        except Error:
            return JsonResponse({'result': {'message': 'Unable to create task database'}})

        return JsonResponse({'result': {'message': 'PAY is successful'}})


urlpatterns = [
    url(r'^$', payment),
]
