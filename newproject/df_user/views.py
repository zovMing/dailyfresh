#coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from hashlib import sha1
from django.core.paginator import Paginator
from . import models
import df_goods
import df_order



def isLogin(func):
    def afterFuck(request,*w,**kwg):
        resp = redirect('/user/login')
        username = request.session.get('username', '')
        if username == "":
            resp.set_cookie('url',request.get_full_path())
            return resp
        else:
            return func(request,*w,**kwg)
    return afterFuck

def register(request):
    return render(request, 'user/register.html')


def register_handle(request):
    #获取表单内容
    post = request.POST
    user_name = post.get('user_name')
    pwd = post.get('pwd')
    cpwd = post.get('cpwd')
    email = post.get('email')
    #表单验证
    if pwd != cpwd:
        return render(request, 'user/register.html')
    #密码加密
    s1 = sha1()
    s1.update(pwd)
    pwd = s1.hexdigest()
    #验证通过，插入数据库
    mUser = models.userInfo()
    mUser.username = user_name
    mUser.uemail = email
    mUser.upwd = pwd
    mUser.save()
    return redirect('/user/login/')

def register_name_handle(request):
    try:
        m = models.userInfo.objects.get(username=request.POST.get('username', ''))
    except models.userInfo.DoesNotExist:
        return JsonResponse({"res":"0"})
    else:
        return JsonResponse({"res":"1"})

def logout(request):
    resp = redirect('/user/login')
    resp.delete_cookie('url')
    del request.session['username']
    return resp

def login(request):
        
    username = request.session.get('username','')
    if username != '':
        del request.session['username']
    username = ''
    isAuto = False
    if request.COOKIES.has_key('username'):
        username = request.COOKIES.get('username')
        isAuto = True
    context = {'username':username, 'isAuto':isAuto}
    res = render(request, 'user/login.html', context)
    gget = request.GET
    if gget.get('no') == 1:
        res.set_cookie('url',"")
    return res

def login_error(request):
    username = ''
    login_serror = '账号或者密码错误'
    isAuto = False
    if request.COOKIES.has_key('username'):
        username = request.COOKIES.get('username')
        isAuto = True
    context = {'username':username, 'isAuto':isAuto, "login_serror":login_serror}
    return render(request, 'user/login.html', context)

def login_handle(request):
    #获取登录表单内容
    post = request.POST
    username = post.get('username')
    pwd = post.get('pwd')
    isAuto = post.get('isAuto')
    try:
        user = models.userInfo.objects.get(username=username)
    except:
        return login_error(request)
    else:
        s1 = sha1()
        s1.update(pwd)
        if user.upwd ==  s1.hexdigest():
            response = ""
            if request.COOKIES.has_key('url'):
                print('qweqweqwe')
                response = redirect(request.COOKIES.get('url'))
            else:
                print('asdasdasd')
                response = redirect( '/user/userInfo/')
            if isAuto == "on":
                response.set_cookie('username',str(username))
            else:
                response.set_cookie('username',' ',max_age=-1)
            request.session['username'] = username
            return response
        else:
            return login_error(request)


@isLogin
def userInfo(request):
    username = request.session.get('username')
    user = models.userInfo.objects.get(username=username)
    uaddress = user.uaddress
    uphone = user.uphone
    if uaddress == "":
        uaddress = "      "
    if uphone  == "":
        uphone = "      "
    lastList = ''
    if request.COOKIES.has_key('lastList'):
        lastList = request.COOKIES.get('lastList')
    olist = []
    lastList = lastList.split(',')
    if not ((len(lastList)==1) and (lastList[0]== '')):
        for i in lastList:
            try:
                z = df_goods.models.GoodsInfo.objects.get(pk=i)
            except df_goods.models.GoodsInfo.DoesNotExist:
                pass
            else:
                olist.append(z)
    context = { 'uaddress':uaddress, 'uphone': uphone, 'username':username, 'olist':olist}
    return render(request, 'user/user_center_info.html', context)
    
@isLogin
def userOrder(request, id):
    if id == '' :
        id = 1
    username = request.session.get('username')
    allOrder = df_order.models.OrderInfo.objects.filter(user__username = username)
    pg = Paginator(allOrder, 2)
    if int(id) >= pg.page_range[-1]:
        id = pg.page_range[-1]
    lst = pg.page(int(id)) 
    allLst = []
    for i in lst:
        z = [i]
        allLst.append(z)
    for i in allLst:
        i.append(df_order.models.OrderDetailInfo.objects.filter(order_id = i[0].oid))
        i.append(df_order.models.OrderDetailInfo.objects.filter(order_id = i[0].oid))
    rrange = pg.page_range
    context = {'allLst':allLst, 'rrange':rrange, 'iid':str(id)}
    return render(request, 'user/user_center_order.html', context)



@isLogin
def userSite(request):
    username = request.session.get('username')
    user = models.userInfo.objects.get(username=username)
    uman = user.uman.encode('utf-8')
    uaddress = ''
    uphone = user.uphone

    if uman != "":
        uman = '{'+uman+'  收  }'
    if user.uaddress != "":
        uaddress = user.uaddress
    if uphone != "":
        uphone = uphone[:3] + '****' + uphone[6:]
    context = {'uman':uman, 'uaddress':uaddress, 'uphone': uphone, 'username':username}
    return render(request, 'user/user_center_site.html', context)
    
@isLogin
def userSite_handle(request):
    #获取信息
    post = request.POST
    uman = post.get('uman')
    uaddress = post.get('uaddress')
    uphone = post.get('uphone')
    #验证

    #更改数据库对应信息
    username = request.session.get('username')
    user = models.userInfo.objects.get(username=username)
    user.uman = uman
    user.uphone = uphone
    user.uaddress = uaddress
    user.save()

    
    return redirect('/user/userSite/')
