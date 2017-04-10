from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'register/', views.register),
    url(r'register_handle/', views.register_handle),
    url(r'login/', views.login),
    url(r'login_handle/', views.login_handle),
    url(r'userInfo/', views.userInfo),
    url(r'userOrder/(\d*)', views.userOrder),
    url(r'userSite/', views.userSite),
    url(r'userSite_handle/', views.userSite_handle),
    url(r'register_name_handle/', views.register_name_handle),
    url(r'logout/', views.logout),
]