#coding=utf-8

from django.conf.urls import url
import views

urlpatterns = [
    url('^$',views.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$',views.list),
    url(r'^(\d+)/$',views.detail),
    url(r'^search/$', views.MySearchView.as_view(),name='search_view'),

]



