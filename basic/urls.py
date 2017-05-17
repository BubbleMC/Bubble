from django.conf.urls import url
from .views import index, success, fail


urlpatterns = [
    url(r'^success/', success),
    url(r'^fail/', fail),
    url(r'^', index)
]