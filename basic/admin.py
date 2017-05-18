#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bubble Copyright © 2017 Il'ya Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from django.contrib import admin
import models


class ItemAdmin(admin.ModelAdmin):
    list_filter = ['item_name']
    list_display = ['item_name', 'item_price']


class MenuAdmin(admin.ModelAdmin):
    list_display = ['menu_name', 'menu_link']


class PaymentAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        if 'is_submitted' in readonly_fields:
            readonly_fields.remove('is_submitted')
        return readonly_fields

    list_display = ['payment_account', 'payment_status', 'payment_dateCreate', 'payment_dateComplete']


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ['task_cmd', 'task_payment']


admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Menu, MenuAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.Task, TaskAdmin)
