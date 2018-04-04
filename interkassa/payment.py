#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2018 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
import hashlib
import base64

from urllib.parse import parse_qsl

from django.urls import re_path
from django.http import Http404, HttpResponse
from django.db import Error
from django.conf import settings

from basic import models


allow_ips = {
    '151.80.190.97',
    '151.80.190.98',
    '151.80.190.99',
    '151.80.190.100',
    '151.80.190.101',
    '151.80.190.102',
    '151.80.190.103',
    '151.80.190.104'
}


required_params = {
    'ik_co_id',
    'ik_am',
    'ik_cur',
    'ik_x_account',
    'ik_x_item',
    'ik_inv_id',
    'ik_inv_st',
    'ik_inv_crt',
    'ik_inv_prc',
    'ik_sign'
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
    account = data.get('ik_x_account')
    key = settings.PAYMENT['secret_key']

    try:
        order_sum = int(data.get('ik_am'))
        item_id = int(data.get('ik_x_item'))
        payment_id = int(data.get('ik_inv_id'))
    except ValueError:
        return HttpResponse('Invalid parameters')

    query_string = request.META.get('QUERY_STRING')
    params = parse_qsl(query_string, keep_blank_values=True)
    params.sort()

    sign_string = ''.join(v + ':' if 'ik_sign' not in k else '' for k, v in params)
    sign_string += key

    sign = base64.b64encode(hashlib.md5(sign_string.encode('utf-8')).digest()).decode()

    if data.get('ik_sign') != sign:
        return HttpResponse('Incorrect digital signature')

    if data.get('ik_inv_st') != 'success':
        return HttpResponse('Invalid payment status')

    if data.get('ik_co_id') != settings.PAYMENT['public_key']:
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
                payment_dateCreate=data.get('ik_inv_crt'),
                payment_dateComplete=data.get('ik_inv_prc')
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
