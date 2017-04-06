from django.db import models
import df_goods
import df_user

class shopcart(models.Model):
    userinfo = models.ForeignKey('df_user.userInfo')
    goodinfo = models.ForeignKey('df_goods.GoodsInfo')
    goodCount = models.IntegerField()