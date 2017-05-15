from django.contrib import admin
from .models import Item, Menu


class ItemAdmin(admin.ModelAdmin):
    list_filter = ['item_name']
    list_display = ['item_name', 'item_price']


class MenuAdmin(admin.ModelAdmin):
    list_display = ['menu_name', 'menu_link']


admin.site.register(Item, ItemAdmin)
admin.site.register(Menu, MenuAdmin)