from django.shortcuts import render
from .models import Item, Menu, Payment
from django.conf import settings

context = {
    'siteName': settings.BUBBLE['siteName'],
    'description': settings.BUBBLE['description'],
    'serverIP': settings.BUBBLE['serverIP'],

    'aggregator': settings.PAYMENT['aggregator'],
    'publicKey': settings.PAYMENT['publicKey'],
}


def index(request):
    context.update({'menus': Menu.objects.all(),
                    'items': Item.objects.all(),
                    'status': -1})

    return render(request, 'index.html', context)


def success(request):
    context.update({'status': 1})

    return render(request, 'index.html', context)


def fail(request):
    context.update({'status': 0})

    return render(request, 'index.html', context)
