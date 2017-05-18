#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings


aggregator = settings.PAYMENT['aggregator'] + '.urls'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^payment/', include(aggregator)),
    url(r'^', include('basic.urls')),
]
