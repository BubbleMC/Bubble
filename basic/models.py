#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


class Item(models.Model):
    class Meta:
        db_table = 'bubble_item'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    item_name = models.CharField(max_length=255, verbose_name='Название')
    item_price = models.IntegerField(verbose_name='Стоимость')
    item_cmd = models.CharField(max_length=255, verbose_name='Команда для выдачи', help_text='Вместо {account} будет подставлен логин покупателя')


class Menu(models.Model):
    class Meta:
        db_table = 'bubble_menu'
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    menu_name = models.CharField(max_length=255, verbose_name='Заголовок')
    menu_link = models.CharField(max_length=255, verbose_name='Ссылка')


class Payment(models.Model):
    class Meta:
        db_table = 'bubble_payment'
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    payment_number = models.IntegerField(default=0, verbose_name='Номер платежа')
    payment_account = models.CharField(max_length=256, verbose_name='Покупатель')
    payment_item = models.ForeignKey(Item, verbose_name='Купленный товар')
    payment_status = models.BooleanField(default=False, verbose_name='Статус платежа')
    payment_dateCreate = models.DateTimeField(default=datetime.now, verbose_name='Дата создания')
    payment_dateComplete = models.DateTimeField(blank=True, null=True, verbose_name='Дата оплаты')


class Task(models.Model):
    class Meta:
        db_table = 'bubble_task'
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    task_cmd = models.CharField(max_length=255, verbose_name='Команда')
    task_payment = models.ForeignKey(Payment, verbose_name='Платёж')
