#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2018 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
import base64
from hashlib import md5, sha256
from urllib.parse import urlencode

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from . import models


args = settings.BUBBLE
args.update({
    'menus': models.Menu.objects.all(),
    'items': models.Item.objects.all()
})


def initialization(request):
    if request.method == 'POST':
        form = request.POST

        item = get_object_or_404(
            models.Item,
            id=form.get('item')
        )

        merchant_id = settings.PAYMENT['public_key']
        secret_key = settings.PAYMENT['secret_key']
        currency = settings.PAYMENT['currency']
        item_id = form.get('item')
        account = form.get('account')
        price = str(item.item_price)
        desc = args['description_of_purchase'].format(
            item=item.item_name,
            account=account,
            project_name=args['project_name']
        )

        aggregator = settings.PAYMENT['aggregator']

        if aggregator == 'unitpay':
            separator = '{up}'
            params = {
                'account': account,
                'currency': currency,
                'desc': desc,
                'sum': price,
            }

            sign_string = separator.join(['{}'.format(value) for (key, value) in params.items()])
            sign_string += separator + secret_key

            sign = sha256(sign_string.encode('utf-8')).hexdigest()
            params.update({'signature': sign})

            params_string = urlencode(params)

            url = 'https://unitpay.ru/pay/{}?{}'
            return redirect(url.format(merchant_id, params_string))

        elif aggregator == 'interkassa':
            separator = ':'
            params = {
                'ik_am': price,
                'ik_co_id': merchant_id,
                'ik_desc': desc,
                'ik_pm_no': 0,
                'ik_x_account': account,
                'ik_x_item': item_id,
            }

            sign_string = separator.join(['{}'.format(value) for (key, value) in params.items()])
            sign_string += separator + secret_key

            sign = base64.b64encode(md5(sign_string.encode('utf-8')).digest())
            params.update({'ik_sign': sign})

            params_string = urlencode(params)

            url = 'https://sci.interkassa.com/?{}'
            return redirect(url.format(params_string))

        elif aggregator == 'free-kassa':
            separator = ':'
            params = {
                'm': merchant_id,
                'oa': price,
                'o': account,
                'i': currency,
                'us_item': item_id
            }

            sign_string = separator.join((merchant_id, price, secret_key, account))

            sign = md5(sign_string.encode('utf-8')).hexdigest()
            params.update({'s': sign})

            params_string = urlencode(params)

            url = 'http://www.free-kassa.ru/merchant/cash.php?{}'
            return redirect(url.format(params_string))

    else:
        return redirect('index')


def index(request):
    return render(request, 'form.html', args)


def pending(request):
    return render(request, 'pending.html', args)


def success(request):
    return render(request, 'success.html', args)


def fail(request):
    return render(request, 'fail.html', args)
