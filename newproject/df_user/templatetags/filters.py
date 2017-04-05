
from django.shortcuts import render, redirect
from . import models

def isLogin(func):
    def afterFuck(request):
        resp = redirect('/user/login')
        resp.set_cookie('url',request.get_full_path)
        print(request.get_full_path)
        username = request.session.get('username', '')
        if username == "":
            return resp
        else:
            return func(request)
    return afterFuck