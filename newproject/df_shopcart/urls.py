from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.index),
    url('^add/', views.add),
    url('^ajaxDel/', views.ajaxDel),
]