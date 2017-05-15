from django.shortcuts import render_to_response
from .models import Item, Menu
from django.conf import settings


def index(request):
    context = {
        'siteName': settings.BUBBLE['siteName'],
        'description': settings.BUBBLE['description'],
        'serverIP': settings.BUBBLE['serverIP'],

        'aggregator': settings.PAYMENT['aggregator'],
        'publicKey': settings.PAYMENT['publicKey'],

        'menus': Menu.objects.all(),
        'items': Item.objects.all()
    }

    return render_to_response('index.html', context)