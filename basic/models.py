from django.db import models


class Settings(models.Model):
    class Meta:
        db_table = 'settings'

    settings_type = models.CharField(max_length=10)
    settings_publicKey = models.CharField(max_length=30, blank=True, default=True)
    settings_secretKey = models.CharField(max_length=30, blank=True, default=True)

class Item(models.Model):
    class Meta:
        db_table = 'item'

    item_price = models.IntegerField()
    item_name = models.CharField(max_length=30)
    item_cmd = models.CharField(max_length=50)
