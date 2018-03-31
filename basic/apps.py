#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2018 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from django.apps import AppConfig


class BasicConfig(AppConfig):
    name = 'basic'
    verbose_name = 'Основное'
    verbose_name_plural = verbose_name
