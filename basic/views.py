#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.conf import settings
from hashlib import md5
import models


context = {
    'siteName': settings.BUBBLE['siteName'],
    'description': settings.BUBBLE['description'],
    'serverIP': settings.BUBBLE['serverIP'],

    'aggregator': settings.PAYMENT['aggregator'],
    'publicKey': settings.PAYMENT['publicKey'],
}


def initialization(request):
    if request.method == 'POST':
        form = request.POST

        try:
            item = models.Item.objects.get(id=form.get('item'))
        except ObjectDoesNotExist:
            return Http404

        id = settings.PAYMENT['publicKey']
        key = settings.PAYMENT['secretKey']
        sum = str(item.item_price)
        account = form.get('account')

        aggr = context['aggregator']

        if aggr == 'unitpay':
            desc = settings.PAYMENT['descriptionOfPurchase'] % (item.item_name, account, context['siteName'])

            return HttpResponseRedirect('https://unitpay.ru/pay/%s?sum=%s&account=%s&desc=%s' % (id, sum,
                                                                                                 account, desc))
        elif aggr == 'interkassa':
            return HttpResponseRedirect('/')

        elif aggr == 'free-kassa':
            sign_string = id + ':' + sum + ':' + key + ':' + account
            sign = md5(sign_string).hexdigest()

            return HttpResponseRedirect('http://www.free-kassa.ru/merchant/cash.php?m=%s&oa=%s&s=%s&o=%s' % (id, sum,
                                                                                                             sign, account))
    else:
        return HttpResponseRedirect('/')


def success(request):
    context.update({'status': 1})

    return render(request, 'index.html', context)


def fail(request):
    context.update({'status': 0})

    return render(request, 'index.html', context)


def index(request):
    context.update({'menus': models.Menu.objects.all(),
                    'items': models.Item.objects.all(),
                    'status': -1})

    return render(request, 'index.html', context)
