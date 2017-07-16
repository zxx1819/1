#coding=utf-8


from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum
from user_log.name_log import *
from models import *

# Create your views here.

def add(request):
    try:
        uid = request.session.get('uid')
        gid = int(request.GET.get('gid'))
        count = int(request.GET.get('count', '1'))
        print gid
        carts = CartInfo.objects.filter(users_id = uid, goods_id = gid)
        if len(carts) == 1:
            cart = carts[0]
            cart.count += count
            cart.save()
        else:
            cart = CartInfo()
            cart.users_id = uid
            cart.goods_id = gid
            cart.count = count
            cart.save()
        return JsonResponse({'isadd':1})

    except:
        return JsonResponse({'isadd':0})


def count(request):
    uid = request.session.get('uid')
    cart_count = CartInfo.objects.filter(users_id = uid).aggregate(Sum('count')).get('count__sum')
    return JsonResponse({'cart_count':cart_count})


@login_valid
def index(request):
    uid = request.session.get('uid')
    cart_list = CartInfo.objects.filter(users_id = uid)
    context = {'title':'购物车','cart_list':cart_list}
    return render(request,'user_cart/cart.html',context)

def edit(request):
    id = int(request.GET.get('id'))
    count = int(request.GET.get('count'))
    cart = CartInfo.objects.get(pk=id)
    cart.count = count
    cart.save()
    return JsonResponse({'ok':1})

def delete(request):
    id = int(request.GET.get('id'))
    cart = CartInfo.objects.get(pk=id)
    cart.delete()
    return JsonResponse({'ok':1})

def order(request):
    user = UserInfo.objects.get(pk = request.session.get('uid'))
    cart_ids = request.POST.getlist('cart_id')
    cart_list = CartInfo.objects.filter(id__in=cart_ids)
    c_ids = ','.join(cart_ids)
    context = {'title':'提交订单','user':user,'cart_list':cart_list,'c_ids':c_ids}
    return render(request,'user_cart/order.html',context)