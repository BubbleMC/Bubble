from django.shortcuts import render_to_response
from .models import Item


def index(request):
    return render_to_response('index.html', {'items': Item.objects.all()})
