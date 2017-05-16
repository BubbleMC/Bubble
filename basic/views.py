from django.shortcuts import render
from .models import Item, Menu, Payment
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

  #  p = Payment(payment_number=123321,
  #              payment_account='Test',
  #              payment_item=Item.objects.get(item_name='VIP'))
  #  p.save()

    return render(request, 'index.html', context)