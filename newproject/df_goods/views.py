#coding=utf-8
from django.shortcuts import render
from . import models
from django.http import HttpResponse
from django.core.paginator import Paginator



def index(request):
    #获取十二个条信息，六个分类下每个分类两块数据：三个倒序id的，代表最新的。四个正序id，代表，，，没啥代表的
    fruits = models.GoodsInfo.objects.filter(gtype=1).order_by('-id')[0:3]
    fruitLs = models.GoodsInfo.objects.filter(gtype=1).order_by('id')[0:4]

    seafoods = models.GoodsInfo.objects.filter(gtype=2).order_by('-id')[0:3]
    seafoodLs = models.GoodsInfo.objects.filter(gtype=2).order_by('id')[0:4]

    meets = models.GoodsInfo.objects.filter(gtype=3).order_by('-id')[0:3]
    meetLs = models.GoodsInfo.objects.filter(gtype=3).order_by('id')[0:4]

    eggs = models.GoodsInfo.objects.filter(gtype=4).order_by('-id')[0:3]
    eggLs = models.GoodsInfo.objects.filter(gtype=4).order_by('id')[0:4]

    vegetabless = models.GoodsInfo.objects.filter(gtype=5).order_by('-id')[0:3]
    vegetablesLs = models.GoodsInfo.objects.filter(gtype=5).order_by('id')[0:4]
    
    ices = models.GoodsInfo.objects.filter(gtype=6).order_by('-id')[0:3]
    iceLs = models.GoodsInfo.objects.filter(gtype=6).order_by('id')[0:4]
    
    context = {'fruits':fruits, 'fruitLs':fruitLs, 'seafoods':seafoods,  'seafoodLs':seafoodLs, 'meets':meets, 'meetLs':meetLs, 'eggs':eggs, 'eggLs':eggLs, 'vegetabless':vegetabless, 'vegetablesLs':vegetablesLs, 'ices':ices, 'iceLs':iceLs}
    return render(request, 'goods/index.html', context)

def detail(request, id):
    try:
        good = models.GoodsInfo.objects.get(pk=id)
        newgood = models.GoodsInfo.objects.filter(gtype=good.gtype).order_by('id')[0:2]
    except models.GoodsInfo.DoesNotExist:
        return HttpResponse('请不要乱来')
    else:
        context = {'good':good, 'newgood':newgood}
        return render(request, 'goods/detail.html', context)

def list(request, id, od, pagid):
    od = int(od)
    goods = None
    if od == 0:
        goods = models.GoodsInfo.objects.filter(gtype=id).order_by('id')
    elif od == 1:
        goods = models.GoodsInfo.objects.filter(gtype=id).order_by('gprice')
    elif od == 2:
        goods = models.GoodsInfo.objects.filter(gtype=id).order_by('gclick')
    if pagid == '':
        pagid = 1
    newgoods = models.GoodsInfo.objects.filter(gtype=id).order_by('gclick')[0:2]

    pagid = int(pagid)
    pag = Paginator(goods, 15)
    pgoods = pag.page(pagid)
    pagrange = pag.page_range
    context = {'pgoods':pgoods, 'pagrange':pagrange, 'newgoods':newgoods, 'pagid':pagid, 'od':od, 'id':id}
    return render(request, 'goods/list.html', context)