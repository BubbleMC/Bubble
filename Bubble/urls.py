#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2018 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings


aggregator = settings.PAYMENT['aggregator'] + '.payment'

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'payment/', include(aggregator), name='payment'),
    path('', include('basic.urls')),
]
