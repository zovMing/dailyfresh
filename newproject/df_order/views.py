#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from hashlib import sha1
from decimal import *
import datetime
from . import models
import df_user
import df_goods
import df_shopcart

@df_user.views.isLogin
def index(request):
    nG = request.GET
    sid = nG.getlist('sid')
    username = request.session.get('username','')
    try:
        ouser = df_user.models.userInfo.objects.get(username = username)
        olgood = df_shopcart.models.shopcart.objects.filter(pk__in = sid)
    except df_user.models.userInfo.DoesNotExist:
        pass
    else:
        context = {'address': ouser.uaddress, 'olgood':olgood}
        return render(request, 'other/place_order.html', context)

@transaction.atomic()
@df_user.views.isLogin
def order_handle(request):
    post = request.POST
    lspid = post.get('lspid')
    address = post.get('address')
    transitCost = post.get('transitCost')
    lcount = post.get('lcount')
    lspid = lspid.split(',')
    tal = post.get('tal')
    print(tal)
    lcount = lcount.split(',')
    username = request.session.get('username')
    time  = datetime.datetime.now()
    sss1 = sha1()
    sss1.update(str(time)+username)
    #设置回滚点
    savepoint = transaction.savepoint()
    issuccess = '1'
    try:
        error = ''
        order = models.OrderInfo()
        order.oid = sss1.hexdigest()
        order.user = df_user.models.userInfo.objects.get(username=username)
        order.odate = time
        order.oIsPay = True
        order.ototal = Decimal(tal)
        #判断账户余额是否充足
        #pass
        order.oaddress = address
        order.save()
        for i in lspid:
            sc = df_shopcart.models.shopcart.objects.get(pk__in=i)
            #判断库存是否充足
            good = sc.goodinfo
            if  good.gkucun > int(lcount[lspid.index(i)]):
                good.gkucun -= int(lcount[lspid.index(i)])
                good.save()
                
                oDetail = models.OrderDetailInfo()
                oDetail.goods_id = good.id
                oDetail.order = order
                oDetail.price = good.gprice
                oDetail.count = lcount[lspid.index(i)]

                print(oDetail.count)
                print(oDetail.goods)
                print(oDetail.order)
                print(oDetail.price)
                oDetail.save()
                sc.delete()
            else:
                error = sc.goodinfo.gtitle+'库存不足'
                transaction.savepoint_rollback(savepoint)
        #成功 提交事务
        transaction.savepoint_commit(savepoint)
    except Exception as e:
        print(e)
        error = str(e)
        issuccess = '0'
        transaction.savepoint_rollback(savepoint)
    finally:
        return JsonResponse({'issuccess':issuccess, 'error':error})