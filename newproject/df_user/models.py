from django.db import models

class userInfo(models.Model):
    username = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=20)
    uaddress = models.CharField(max_length=100,default='')
    uphone = models.CharField(max_length=11,default='')
    uman = models.CharField(max_length=20,default='')
