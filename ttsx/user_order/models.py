# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from user_log.models import UserInfo
from user_goods.models import GoodsInfo
# Create your models here.

class OrderMain(models.Model):
    order_id = models.CharField(max_length=30, primary_key=True)
    user = models.ForeignKey(UserInfo)
    order_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    state = models.IntegerField(default=0)


class OrderDetail(models.Model):
    order = models.ForeignKey(OrderMain)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
