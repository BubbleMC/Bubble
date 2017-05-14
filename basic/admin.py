from django.contrib import admin
from .models import Settings, Item


class SettingsAdmin(admin.ModelAdmin):
    fields = ['settings_type','settings_publicKey']
    list_filter = ['settings_type']
    list_display = ['settings_type', 'settings_publicKey']

class ItemAdmin(admin.ModelAdmin):
    list_filter = ['item_name']
    list_display = ['item_name', 'item_price']

admin.site.register(Settings, SettingsAdmin)
admin.site.register(Item, ItemAdmin)