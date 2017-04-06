#coding=utf-8
from django.shortcuts import render
from . import models
from django.http import HttpResponse
from django.core.paginator import Paginator
import df_shopcart



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
    qwe = request.session.get('username', '')
    goodcount = 0
    if qwe != '':
        goodcount = df_shopcart.models.shopcart.objects.filter(userinfo__username = qwe).count()
    
    
    context = {'fruits':fruits, 'fruitLs':fruitLs, 'seafoods':seafoods,  'seafoodLs':seafoodLs, 'meets':meets, 'meetLs':meetLs, 'eggs':eggs, 'eggLs':eggLs, 'vegetabless':vegetabless, 'vegetablesLs':vegetablesLs, 'ices':ices, 'iceLs':iceLs, 'ct':goodcount}
    return render(request, 'goods/index.html', context)

def detail(request, id):
    try:
        good = models.GoodsInfo.objects.get(pk=id)
        newgood = models.GoodsInfo.objects.filter(gtype=good.gtype).order_by('id')[0:2]
    except models.GoodsInfo.DoesNotExist:
        return HttpResponse('请不要乱来')
    else:
        #讲id存入一个数组存入cookie中。
        lastList = ''
        if request.COOKIES.has_key('lastList'):
            lastList = request.COOKIES.get('lastList')
        lastList = getList(lastList, id)
        qwe = request.session.get('username', '')
        goodcount = 0
        if qwe != '':
            goodcount = df_shopcart.models.shopcart.objects.filter(userinfo__username = qwe).count()
        context = {'good':good, 'newgood':newgood, 'ct':goodcount}
        reps = render(request, 'goods/detail.html', context)
        reps.set_cookie('lastList', lastList)
        return reps

def getList(lst, x):
    '''
        将最后一个id移除，新的id放在0下标的列表中。
    '''
    if lst == '':
        lst += x
        return lst
    else:
        lst = lst.split(',')
        if x in lst:
            lst.remove(x)
        elif len(lst) < 5:
            pass
        else:
            del lst[len(lst)-1]
        lst.insert(0, x)
    return ','.join(lst)


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
    qwe = request.session.get('username', '')
    goodcount = 0
    if qwe != '':
        goodcount = df_shopcart.models.shopcart.objects.filter(userinfo__username = qwe).count()
    context = {'pgoods':pgoods, 'pagrange':pagrange, 'newgoods':newgoods, 'pagid':pagid, 'od':od, 'id':id, 'ct':goodcount}
    return render(request, 'goods/list.html', context)