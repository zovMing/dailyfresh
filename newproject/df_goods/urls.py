from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^$', views.index),
    url(r'^detail/([0-9]+)', views.detail),
    url(r'^list/([1-6])/([0-2])/([0-9]*)', views.list),
]