#coding=utf-8
from django.shortcuts import render, redirect
import df_user
import df_goods
from . import models
from django.http import JsonResponse
from django.db.models import Q

@df_user.views.isLogin
def index(request):
    username = request.session.get('username','')
    print(username)
    fuckyou = models.shopcart.objects.filter(Q(userinfo__username=username))
    for i in fuckyou:
        print(i)
    lt = []
    ct = len(fuckyou)
    if ct != 0 :
        lt = fuckyou
    context = {'lt':lt, 'ct':ct}
    return render(request, 'other/cart.html', context)

def add(request):
    post = request.POST
    sid = post.get('sid', '')
    snum = post.get('snum', '')
    username = request.session.get('username','')
    if username == '':
        return JsonResponse({'nologin':'1'})
    try:
        oUser = df_user.models.userInfo.objects.get(username=username)
        oGood = df_goods.models.GoodsInfo.objects.get(id=int(sid))
    except df_user.models.userInfo.DoesNotExist:
        return JsonResponse({'s':'false'})
    except df_goods.models.GoodsInfo.DoesNotExist:
        return JsonResponse({'s':'false'})

    else:
        z = models.shopcart.objects.filter(Q(userinfo__username=username)&Q(goodinfo__id=sid))
        if z.count() ==0 :
            print('-------------------')
            newCart = models.shopcart()
            newCart.userinfo = oUser
            newCart.goodinfo = oGood
            newCart.goodCount = int(snum)
            newCart.save()
        else:
            cart = z[0]
            cart.goodCount += int(snum)
            cart.save()
        if post.get('go','')=='':
            cartCount = models.shopcart.objects.filter(userinfo_id=oUser.id).count()
            return JsonResponse({'s':'true', 'num':cartCount})
        else:
            mt = request.META
            ress ='/shopcart/'
            return JsonResponse({'s':'true', 'ress':ress})

def ajaxDel(request):
    post = request.POST
    sid = post.get('sid', '')
    print(sid)
    username = request.session.get('username','')
    if username == '':
        return JsonResponse({'nologin':'1'})
    oz = None
    try:
        oz = models.shopcart.objects.get(pk=sid)
    except models.shopcart.DoesNotExist:        
        context = {'res':1}
        return JsonResponse(context)
    else:
        oz.delete()
        context = {'res':1}
        return JsonResponse(context)