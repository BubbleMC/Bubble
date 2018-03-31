#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2018 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from django.urls import path

from . import views


urlpatterns = [
    path('redirect/', views.initialization, name='redirect'),
    path('pending/', views.pending, name='pending'),
    path('success/', views.success, name='success'),
    path('fail/', views.fail, name='fail'),
    path('', views.index, name='index')
]
