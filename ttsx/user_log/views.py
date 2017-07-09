#coding=utf-8

from django.shortcuts import render , redirect
from django.http import HttpResponse,JsonResponse
from hashlib import sha1
from models import *
import datetime
from name_log import *  #验证是否登陆装饰器包

# Create your views here.


def register(request):
    context = {'title':'注册','top':'0'}
    return render(request,'user_log/register.html',context)


def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    umail = post.get('user_email')
    #sha1加密
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    # 存到数据库
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_sha1
    user.umail = umail
    user.save()

    return redirect('/user/login/')


def register_valid(request):
    uname = request.GET.get('uname')
    result = UserInfo.objects.filter(uname=uname).count()
    context = {'valid':result}
    return JsonResponse(context)



def login(request):
    context = {'title':'登陆','top':'0'}
    return render(request,'user_log/login.html',context)


def login_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    uname_yz = post.get('name_jz','0')
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    context = {'title':'登陆','uname':uname,'upwd':upwd}
    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 0:
        #账号错误
        context['name_error'] = '1'
        return render(request, 'user_log/login.html', context)
    else:
        if users[0].upwd == upwd_sha1:#登陆成功
            request.session['uid'] = users[0].id
            request.session['uname'] = uname
            path = request.session.get('url_path','/')
            response = redirect(path)

            if uname_yz == '1':
                response.set_cookie('uname',uname,expires=datetime.datetime.now() + datetime.timedelta(days = 7))
            else:
                response.set_cookie('uname','',max_age=-1)

            return response
        else:  #密码错误
            context['pwd_error'] = '1'
            return render(request, 'user_log/login.html', context)

 #验证是否登陆装饰器
@login_valid
def center(request):

    user = UserInfo.objects.get(pk=request.session['uid'])
    context = {'title':'用户中心','user':user}
    return render(request,'user_log/center.html',context)

@login_valid
def order(request):
    context = {'title': '用户中心'}
    return render(request, 'user_log/order.html', context)

@login_valid
def site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method == 'POST':
        post = request.POST
        user.ushow = post.get('ushow')
        user.uaddress = post.get('uaddress')
        user.ucode = post.get('ucode')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心','user':user}
    return render(request, 'user_log/site.html', context)


def logout(request):
    request.session.flush()
    return redirect('/user/login/')




