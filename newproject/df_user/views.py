#coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from hashlib import sha1
from . import models

def register(request):
    return render(request, 'user/register.html')
def isLogin(func):
    def afterFuck(request):
        username = request.session.get('username', '')
        if username == "":
            return redirect('/user/login')
        else:
            print(username)
            return func(request)
    return afterFuck

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
    return render(request, 'user/login.html', context)

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
    context = { 'uaddress':uaddress, 'uphone': uphone, 'username':username}
    return render(request, 'user/user_center_info.html', context)
    
@isLogin
def userOrder(request):
    return render(request, 'user/user_center_order.html')
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
