from django.contrib import admin
from . import models

class TypeList(admin.ModelAdmin):
    list_display = ('ttitle','isDelete')

class GoodsList(admin.ModelAdmin):
    list_display=('gtitle')

admin.site.register(models.GoodsInfo)
admin.site.register(models.TypeInfo, TypeList)