from django.db import models

# Create your models here.


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    umail = models.CharField(max_length=20)
    ushou = models.CharField(max_length=10,default='')
    uaddress = models.CharField(max_length=100,default='')
    ucode = models.CharField(max_length=6,default='')
    uphone = models.CharField(max_length=11,default='')