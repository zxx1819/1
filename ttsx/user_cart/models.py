from django.db import models
from user_goods.models import GoodsInfo
from user_log.models import UserInfo
# Create your models here.

class CartInfo(models.Model):
    users = models.ForeignKey('user_log.UserInfo')
    goods = models.ForeignKey('user_goods.GoodsInfo')
    count = models.IntegerField()