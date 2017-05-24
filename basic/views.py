#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from __future__ import unicode_literals

import base64
from hashlib import md5

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.conf import settings
import models


context = {
    'siteName': settings.BUBBLE['siteName'],
    'description': settings.BUBBLE['description'],
    'serverIp': settings.BUBBLE['serverIp'],

    'aggregator': settings.PAYMENT['aggregator'],
    'publicKey': settings.PAYMENT['publicKey'],
}


def initialization(request):
    if request.method == 'POST':
        form = request.POST

        try:
            item = models.Item.objects.get(id=form.get('item'))
        except ObjectDoesNotExist:
            raise Http404

        id = settings.PAYMENT['publicKey']
        key = settings.PAYMENT['secretKey']
        itemId = form.get('item')
        account = form.get('account')
        price = str(item.item_price)
        desc = settings.BUBBLE['descriptionOfPurchase'].format(item=item.item_name,
                                                               account=account,
                                                               siteName=context['siteName'])

        aggr = context['aggregator']

        if aggr == 'unitpay':
            url = 'https://unitpay.ru/pay/{}?sum={}&account={}[{}]%&desc={}'
            return redirect(url.format(id, price, account, itemId, desc))
        elif aggr == 'interkassa':
            signString = price + ':' + id + ':' + desc + ':0:' + account + ':' + itemId + ':' + key
            sign = base64.b64encode(md5(signString.encode('utf-8')).digest())

            url = 'https://sci.interkassa.com/?ik_co_id={}&ik_am={}&ik_desc={}&ik_x_item={}&ik_x_account={}&ik_pm_no=0&ik_sign={}'
            return redirect(url.format(id, price, desc, itemId, account, sign))
        elif aggr == 'free-kassa':
            signString = id + ':' + price + ':' + key + ':' + account
            sign = md5(signString.encode('utf-8')).hexdigest()

            url = 'http://www.free-kassa.ru/merchant/cash.php?m={}&oa={}&s={}&o={}&us_item={}'
            return redirect(url.format(id, price, sign, account, itemId))
    else:
        return redirect('/')


def success(request):
    context.update({'status': 1})

    return render(request, 'index.html', context)


def fail(request):
    context.update({'status': 0})

    return render(request, 'index.html', context)


def index(request):
    context.update({'menus': models.Menu.objects.all(), 'items': models.Item.objects.all(), 'status': -1})

    return render(request, 'index.html', context)
