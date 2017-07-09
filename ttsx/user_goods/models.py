#coding=utf-8

from django.db import models
from tinymce.models import HTMLField
# Create your models here.

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=30)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')

class GoodsInfo(models.Model):

    gtitle=models.CharField(max_length=50) #图片名
    gpic=models.ImageField(upload_to='goods') #图片
    gprice=models.DecimalField(max_digits=7,decimal_places=2)#价格 999999.99
    gclick = models.IntegerField(default=0) #点击量
    gunit=models.CharField(max_length=20)  #单位
    isDelete = models.BooleanField(default=False)  #是否删除
    gsubtitle=models.CharField(max_length=200) #简介
    gkucun = models.IntegerField(default=100) #库存
    gcontent=HTMLField()                            #详细介绍
    gtype=models.ForeignKey('TypeInfo') #对的类

