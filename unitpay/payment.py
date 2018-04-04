#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2018 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
import re
from hashlib import sha256
from urllib.parse import parse_qsl

from django.utils import timezone
from django.urls import re_path
from django.db import Error
from django.http import Http404, JsonResponse
from django.conf import settings

from basic import models


allowIps = {
    '31.186.100.49',
    '178.132.203.105',
    '52.29.152.23',
    '52.19.56.234'
}


getParameters = {
    'method',
    'params[account]',
    'params[signature]',
    'params[unitpayId]',
    'params[orderSum]',
    'params[orderCurrency]'
}


def payment(request):
    ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if ip is None:
        ip = request.META.get('REMOTE_ADDR')

    if ip not in allowIps:
        raise Http404()

    for getParameter in getParameters:
        if getParameter not in request.GET:
            return JsonResponse({'error': {'message': 'Invalid request'}})

    data = request.GET.copy()
    method = data.get('method')
    key = settings.PAYMENT['secret_key']
    currency = settings.PAYMENT['currency']

    try:
        order_sum = int(data.get('params[orderSum]'))
        account = re.findall(r'(.*)(?=\[)', data.get('params[account]'))[0]
        item_id = int(re.findall(r'(?<=\[)(.*)(?=\])', data.get('params[account]'))[0])
        payment_id = int(data.get('params[unitpayId]'))
    except ValueError:
        return JsonResponse({'error': {'message': 'Invalid parameters'}})
    except IndexError:
        return JsonResponse({'error': {'message': 'Invalid account'}})

    query_string = request.META.get('QUERY_STRING')
    params = parse_qsl(query_string, keep_blank_values=True)
    params.sort()

    sign_string = ''
    for param in params:
        if (param[0] != 'params[sign]') and (param[0] != 'params[signature]'):
            sign_string += param[1] + '{up}'
    sign_string += key

    sign = sha256(sign_string.encode('utf-8')).hexdigest()

    if data.get('params[signature]') != sign:
        return JsonResponse({'error': {'message': 'Incorrect digital signature'}})

    if method == 'check':
        try:
            payment = models.Payment.objects.get(payment_number=payment_id)
        except models.Payment.DoesNotExist:
            try:
                item = models.Item.objects.get(id=item_id)
            except models.Payment.DoesNotExist:
                return JsonResponse({'error': {'message': 'Invalid purchase subject'}})

            price = item.item_price

            if price != order_sum:
                return JsonResponse({'error': {'message': 'Invalid payment amount'}})
            if currency != data.get('params[orderCurrency]'):
                return JsonResponse({'error': {'message': 'Invalid payment currency'}})

            try:
                payment = models.Payment(
                    payment_number=payment_id,
                    payment_account=account,
                    payment_item=item
                )
                payment.save()

                return JsonResponse({'result': {'message': 'CHECK is successful'}})
            except Error:
                return JsonResponse({'error': {'message': 'Unable to create payment database'}})
        else:
            return JsonResponse({'result': {'message': 'Payment already exists'}})

    if method == 'pay':
        try:
            payment = models.Payment.objects.get(payment_number=payment_id)
        except models.Payment.DoesNotExist:
            return JsonResponse({'error': {'message': 'Payment not found'}})

        if payment.payment_status == 1:
            return JsonResponse({'result': {'message': 'Payment has already been paid'}})

        try:
            payment.payment_status = 1
            payment.payment_dateComplete = timezone.now()
            payment.save()
        except Error:
            return JsonResponse({'error': {'message': 'Unable to confirm payment database'}})

        try:
            item = models.Item.objects.get(id=item_id)
            cmd = item.item_cmd.format(account=account)

            task = models.Task(
                task_cmd=cmd,
                task_payment=payment
            )
            task.save()

            return JsonResponse({'result': {'message': 'PAY is successful'}})
        except models.Item.DoesNotExist:
            return JsonResponse({'error': {'message': 'Invalid purchase subject'}})
        except Error:
            return JsonResponse({'error': {'message': 'Unable to create task database'}})

    return JsonResponse({'error': {'message': 'Method not supported'}})


urlpatterns = [
    re_path(r'^$', payment),
]
