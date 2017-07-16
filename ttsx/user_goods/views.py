#coding=utf-8

from django.shortcuts import render , redirect
from models import *
from django.core.paginator import Paginator
from haystack.generic_views import SearchView
# Create your views here.

def index(request):
    '''首页'''
    goods_list = []

    type_list = TypeInfo.objects.all()

    for t1 in type_list:
        nlist = t1.goodsinfo_set.order_by('-id')[0:4]
        clist = t1.goodsinfo_set.order_by('-gclick')[0:4]
        goods_list.append({'t1':t1,'nlist':nlist,'clist':clist})  #{[{}]}
    context = {'title':'首页','glist':goods_list,'cart_show':'1'}
    return render(request,'user_goods/index.html',context)


def list(request, tid, pindex, orderby):

    try:
        t1 = TypeInfo.objects.get(pk = int(tid))
        new_list = t1.goodsinfo_set.order_by('-id')[0:2]
        orderby_str = '-id'
        desc = '1'
        if orderby == '2':
            desc = request.GET.get('desc','1')
            if desc == '1':
                orderby_str = '-gprice'
            else:
                orderby_str = 'gprice'
        elif orderby == '3':
            orderby_str = 'gclick'

        glist = t1.goodsinfo_set.order_by(orderby_str)
        paginator = Paginator(glist,15)
        pindex1 = int(pindex)
        if pindex1 < 1:
            pindex1 = 1
        elif pindex1 > paginator.num_pages:
            pindex1 = paginator.num_pages
        page = paginator.page(pindex1)

        if page.paginator.num_pages < 5:
            page_range = page.paginator.page_range
        elif page.number <= 2:
            page_range = range(1, 6)
        elif page.number >= page.paginator.num_pages -1:
            page_range = range(page.paginator.num_pages -4, page.paginator.num_pages +1)
        else:
            page_range = range(page.number -2, page.number +3)
        context = {'title':'商品列表',
                   'cart_show':'1',
                   't1':t1,
                   'new_list':new_list,
                   'page':page,
                   'orderby':orderby,
                   'desc':desc,
                   'page_range':page_range,
                   }
        return render(request,'user_goods/list.html',context)
    except:
        return render(request,'404.html')


def detail(request,id):
    try:
        goods = GoodsInfo.objects.get(pk=int(id))
        goods.gclick += 1
        goods.save()
        new_list = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context = {'title': '商品详情','cart_show':'1','goods':goods,'new_list':new_list}
        response = render(request, 'user_goods/detail.html', context)
        gids = request.COOKIES.get('goods_ids','').split(',')
        if id in gids:
            gids.remove(id)
        gids.insert(0,id)
        if len(gids) > 6:
            gids.pop()
        response.set_cookie('goods_ids',','.join(gids),max_age=60*60*24*7)
        return response

    except:
        return render(request,'404.html')

class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['cart_show']='1'
        page_range=[]
        page=context.get('page_obj')
        if page.paginator.num_pages<5:
            page_range=page.paginator.page_range
        elif page.number<=2:#第1、2页
            page_range=range(1,6)
        elif page.number>=page.paginator.num_pages-1:#倒数第1、2页 6 7 8 9 10
            page_range=range(page.paginator.num_pages-4,page.paginator.num_pages+1)
        else:# 3 4 5 6 7
            page_range=range(page.number-2,page.number+3)
        context['page_range']=page_range
        return context



# page_range = []
# if page.paginator.num_pages < 5:
#     page_range = page.paginator.page_range
# elif page.number <= 2:  # 第1、2页
#     page_range = range(1, 6)
# elif page.number >= page.paginator.num_pages - 1:  # 倒数第1、2页 6 7 8 9 10
#     page_range = range(page.paginator.num_pages - 4, page.paginator.num_pages + 1)
# else:  # 3 4 5 6 7
#     page_range = range(page.number - 2, page.number + 3)

'''
    列表页：排序，页码控制
    最近浏览
    全文检索

    购物车：模型类，视图，模板，列表页购买，详细页购买，
    订单：模型类，购买，事务处理
'''

