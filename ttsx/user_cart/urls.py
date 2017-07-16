# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.index),
    url(r'^count/$',views.count),
    url('^add/$',views.add),
    url('^edit/$',views.edit),
    url('^delete/$',views.delete),
    url('^order/$',views.order),
]