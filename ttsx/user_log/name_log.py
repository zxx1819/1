
#coding=utf-8

from django.shortcuts import redirect


def login_valid(func):
    def func1(request,*args,**kwargs):
        if request.session.has_key('uid'):
            return func(request,*args,**kwargs)
        else:
            return redirect('/user/login/')
    return func1