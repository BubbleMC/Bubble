from django.db import models


class Item(models.Model):
    class Meta:
        db_table = 'bubble_item'

    item_price = models.IntegerField(unique=True)
    item_name = models.CharField(max_length=255)
    item_cmd = models.CharField(max_length=255)


class Menu(models.Model):
    class Meta:
        db_table = 'bubble_menu'

    menu_name = models.CharField(max_length=255)
    menu_link = models.CharField(max_length=255)
