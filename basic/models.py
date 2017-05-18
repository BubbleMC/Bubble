#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from django.db import models
from datetime import datetime


class Item(models.Model):
    class Meta:
        db_table = 'bubble_item'

    item_price = models.IntegerField()
    item_name = models.CharField(max_length=255)
    item_cmd = models.CharField(max_length=255)


class Menu(models.Model):
    class Meta:
        db_table = 'bubble_menu'

    menu_name = models.CharField(max_length=255)
    menu_link = models.CharField(max_length=255)


class Payment(models.Model):
    class Meta:
        db_table = 'bubble_payment'

    payment_number = models.IntegerField(default=0)
    payment_account = models.CharField(max_length=256)
    payment_item = models.ForeignKey(Item)
    payment_status = models.BooleanField(default=False)
    payment_dateCreate = models.DateTimeField(default=datetime.now())
    payment_dateComplete = models.DateTimeField(blank=True, null=True)


class Task(models.Model):
    class Meta:
        db_table = 'bubble_task'

    task_cmd = models.CharField(max_length=255)
    task_payment = models.ForeignKey(Payment)
