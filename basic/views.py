#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2018 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
import base64
from hashlib import md5

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from . import models


args = {
    'site_title': settings.BUBBLE['site_title'],
    'project_name': settings.BUBBLE['project_name'],
    'keywords': settings.BUBBLE['keywords'],
    'description': settings.BUBBLE['description'],
    'server_ip': settings.BUBBLE['server_ip'],

    'aggregator': settings.PAYMENT['aggregator'],
    'public_key': settings.PAYMENT['public_key'],
}


def initialization(request):
    if request.method == 'POST':
        form = request.POST

        item = get_object_or_404(
            models.Item,
            id=form.get('item')
        )

        cash = settings.PAYMENT['public_key']
        secret_key = settings.PAYMENT['secret_key']
        item_id = form.get('item')
        account = form.get('account')
        price = str(item.item_price)
        desc = settings.BUBBLE['description_of_purchase'].format(
            item=item.item_name,
            account=account,
            project_name=args['project_name']
        )

        aggregator = args['aggregator']

        if aggregator == 'unitpay':
            url = 'https://unitpay.ru/pay/{}?sum={}&account={}[{}]%&desc={}'
            return redirect(url.format(cash, price, account, item_id, desc))

        elif aggregator == 'interkassa':
            sign_string = price + ':' + cash + ':' + desc + ':0:' + account + ':' + item_id + ':' + secret_key
            sign = base64.b64encode(md5(sign_string.encode('utf-8')).digest())

            url = 'https://sci.interkassa.com/?ik_co_id={}&ik_am={}' \
                  '&ik_desc={}&ik_x_item={}&ik_x_account={}&ik_pm_no=0&ik_sign={}'
            return redirect(url.format(cash, price, desc, item_id, account, sign))

        elif aggregator == 'free-kassa':
            sign_string = cash + ':' + price + ':' + secret_key + ':' + account
            sign = md5(sign_string.encode('utf-8')).hexdigest()

            url = 'http://www.free-kassa.ru/merchant/cash.php?m={}&oa={}&s={}&o={}&us_item={}'
            return redirect(url.format(cash, price, sign, account, item_id))

    else:
        return redirect('index')


def index(request):
    args.update(
        {
            'menus': models.Menu.objects.all(),
            'items': models.Item.objects.all()
        }
    )

    return render(request, 'form.html', args)


def pending(request):
    message = settings.BUBBLE['messageOfPending']
    args.update(
        {
            'message': message
        }
    )

    return render(request, 'pending.html', args)


def success(request):
    message = settings.BUBBLE['messageOfSuccess']
    args.update(
        {
            'message': message
        }
    )

    return render(request, 'success.html', args)


def fail(request):
    message = settings.BUBBLE['messageOfFail']
    args.update(
        {
            'message': message
        }
    )

    return render(request, 'fail.html', args)
