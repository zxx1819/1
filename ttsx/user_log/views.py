#coding=utf-8

from django.shortcuts import render , redirect
from django.http import HttpResponse,JsonResponse
from hashlib import sha1
from models import *
import datetime
from name_log import *  #验证是否登陆装饰器包
from user_goods.models import GoodsInfo
from user_order.models import *
from django.core.paginator import Paginator

# Create your views here.


def register(request):
    '''项目注册'''
    context = {'title':'注册','top':'0'}  #传title，默认值，不为0执行另一个逻辑
    return render(request,'user_log/register.html',context)


def register_handle(request):
    '''注册管理'''
    post = request.POST  #获取request的POST属性
    uname = post.get('user_name') #获取input值
    upwd = post.get('user_pwd')
    umail = post.get('user_email')
    #sha1加密
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()

    user = UserInfo()
    user.uname = uname   # 存到数据库
    user.upwd = upwd_sha1
    user.umail = umail
    user.save()

    return redirect('/user/login/') #注册成功中定向到登陆页


def register_valid(request):
    uname = request.GET.get('uname')  #获取当前用户名
    result = UserInfo.objects.filter(uname=uname).count()   #查看name总数
    context = {'valid':result}
    return JsonResponse(context)  #返回Json数据



def login(request):
    context = {'title':'登陆','top':'0'}
    return render(request,'user_log/login.html',context)


def islogin(request):
    result = 0
    if request.session.has_key('uid'):
        result = 1
    return JsonResponse({'islogin':result})

# noinspection SpellCheckingInspection
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
    gids = request.COOKIES.get('goods_ids','').split(',')
    gids.pop()
    glist = []
    for gid in gids:
        glist.append(GoodsInfo.objects.get(id = gid))
    context = {'title':'用户中心','user':user,'glist':glist}
    return render(request,'user_log/center.html',context)

@login_valid
def order(request):
    pindex = int(request.GET.get('pindex', '1'))
    uid = request.session.get('uid')
    order_list = OrderMain.objects.filter(user_id=uid).order_by('-order_date')
    paginator = Paginator(order_list,1)
    order_page = paginator.page(pindex)

    #分页
    page_list = []
    if paginator.num_pages < 5:
        page_list = paginator.page_range
    elif order_page.number <= 2:
        page_list = range(1, 6)
    elif order_page.number > paginator.num_pages -1:
        page_list = range( paginator.num_pages - 4, paginator.num_pages + 1)
    else:
        page_list = range(pindex -2, pindex +3)

    context = {'title': '用户中心','order_page':order_page,'page_list':page_list}
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




