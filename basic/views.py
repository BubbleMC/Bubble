#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
import models


context = {
    'siteName': settings.BUBBLE['siteName'],
    'description': settings.BUBBLE['description'],
    'serverIP': settings.BUBBLE['serverIP'],

    'aggregator': settings.PAYMENT['aggregator'],
    'publicKey': settings.PAYMENT['publicKey'],
}


def initialization(request):
    test = 'Проверка редиректа'
    return HttpResponseRedirect('https://unitpay.ru/pay/%s?sum=10&account=%s&desc=%s' % (context['publicKey'],  context['siteName'], test))


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
