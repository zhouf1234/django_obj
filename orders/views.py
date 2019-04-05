from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import JsonResponse
from school.models import Schools
from major.models import Majors,MajorCates
from user.models import Users
from .models import Orders
# Create your views here.

#报名信息展示
def orderList(request):
    order = Orders.objects.filter(is_status=1)
    context ={'order':order}
    return render(request,'order/order_list.html',context=context)

#查看报名信息详情
def detailOrd(request):
    ord_id = request.POST.get('ord_id',None)
    order = Orders.objects.get(id=ord_id)
    return render(request,'order/detailord.html',context={'order':order})

#编辑报名详情:接收数据
#相同专业名，相同层次，不同学校，显示时使之层次也只显示一次；同时改写了get_level
def editOrd(request):
    ord_id = request.GET.get('ord_id',None)
    order = Orders.objects.get(id=ord_id)
    ord_school = Schools.objects.filter(is_status=1)
    user = Users.objects.filter(is_status=1)
    major = Majors.objects.filter(is_status=1).exclude(major_name=order.major.major_name)
    majors = Majors.objects.filter(major_name=order.major.major_name,is_status=1).exclude(level=order.order_level.level)
    # print(majors)
    o_mj = Majors.objects.values('level').distinct().filter(is_status=1).exclude(level=order.order_level.level)
    # print(o_mj)
    o_mj_lis = []
    for i in o_mj:      #再通过层次和名称取到符合条件的第一个
        o_mj2 = Majors.objects.filter(level=i['level'],major_name=order.major.major_name).first()
        if o_mj2 != None:
            o_mj_lis.append(o_mj2)
    # print(o_mj_lis)
    majorss = Majors.objects.filter(major_name=order.major.major_name,level=order.order_level.level,is_status=1).exclude(school=order.order_school.id)
    major_cates = MajorCates.objects.filter(is_status=1).exclude(catename=order.major_cates.catename)
    context = {
        'order':order,
        'user':user,
        'major':major,
        'major_cates':major_cates,
        'ord_school':ord_school,
        'majors':majors,
        'majorss':majorss,
        'o_mj_lis':o_mj_lis,
    }
    return render(request,'order/edit_ord.html',context=context)

#获取专业分类信息,因为专业名称有相同，所以必须用重新写的,按get_catess，其实俩一样的，用于edit_ord0.html了
def get_cates(request):
    catesid = request.POST.get('catesid',None)
    info = Majors.objects.filter(major_category_id=catesid,is_status=1)
    # print(info)
    # list = []
    # for item in info.all():
    #     list.append([item.id,item.major_name])

    lis = []
    lis2=[]
    for ite in info.all():
        if ite.major_name not in lis:
            lis.append(ite.major_name)
    print(lis)
    for i in lis:
        info1 = Majors.objects.filter(major_name=i).first()
        # print(info1.id)
        lis2.append(info1.id)
    print(lis2)
    #接下来就是把列表合并为一个，就可
    listss =[]
    lists = list(zip(lis2, lis))
    for item in lists:
        listss.append([item[0], item[1]])
    return JsonResponse({'data':listss})

#获取院校信息，通过专业列表的id，得到专业名，再得到专业名匹配到的所有院校id，按get_schools，用于edit_ord0.html了
def get_school(request):
    schoolid = request.POST.get('schoolid',None)
    # print(schoolid)
    info = Majors.objects.get(id=schoolid)
    info2 = Majors.objects.filter(major_name=info.major_name)
    # print(info2)
    list = []
    for item in info2.all():
        list.append([item.school_id,item.school.name])
    return JsonResponse({'data':list})
    # return HttpResponse(123)

#编辑报名信息：上传数据，层次已补上
def updateOrd(request):
    # 获取数据
    data = request.POST.get('data', None)
    orderid = request.POST.get('ord_id', None)

    data = json.loads(data)
    order = Orders.objects.get(id=orderid)
    # print(data)
    if data['major_cates'] != '':
        order.major_cates = MajorCates.objects.get(id=data['major_cates'])
        if data['major'] != '':
            order.major = Majors.objects.get(id=data['major'])
            # print(order.major)
            if data['order_level'] !='':
                mj =Majors.objects.get(id=data['major'])
                # print(mj.major_name)
                # print(data['order_level'])
                order.order_level = Majors.objects.get(major_name=mj.major_name,level=data['order_level'],is_status=1,school_id=data['order_school'])
                # print(order.order_level)
                if data['order_school'] !='':
                    # print(data['order_school'])
                    order.order_school = Schools.objects.get(id=data['order_school'])

    if data['real_name'] != '':
        order.real_name = data['real_name']

    if data['phone'] != '':
        order.phone = data['phone']

    if data['idcard'] != '':
        order.idcard = data['idcard']

    if data['status'] != '':
        order.status = data['status']

    order.save()
    return JsonResponse({
        "status": "success",
        "message": "信息更改成功",
        "info": ""
    })

#添加报名信息:获取新页面，添加报名信息页面
#上传时，所有的都不允许为空，参考major的添加，前四项都不允许为空，要写正则判断；用户id这里要写判断是否存在
def addOrd(request):
    major = Majors.objects.filter(is_status=1)
    major_cates = MajorCates.objects.filter(is_status=1)
    context = {
        'major': major,
        'major_cates': major_cates,
    }
    return render(request, 'order/add_ord.html',context=context)

#获取专业分类信息,因为专业名称有相同，所以必须用重新写的
def get_catess(request):
    catesid = request.POST.get('catesid',None)
    info = Majors.objects.filter(major_category_id=catesid,is_status=1)
    # print(info)
    # list = []
    # for item in info.all():
    #     list.append([item.id,item.major_name])

    lis = []
    lis2=[]
    for ite in info.all():              #按此，是因为，如果几个专业名称相同也只会往列表存一个
        if ite.major_name not in lis:
            lis.append(ite.major_name)
    # print(lis)
    for i in lis:
        info1 = Majors.objects.filter(major_name=i).first() #按上方获取的名称取得第一个id
        # print(info1.id)
        lis2.append(info1.id)
    # print(lis2)
    #接下来就是把列表合并为一个，就可
    listss =[]
    lists = list(zip(lis2, lis))
    for item in lists:
        listss.append([item[0], item[1]])
    return JsonResponse({'data':listss})

#获取专业层次信息，通过专业列表的id，得到专业名，再得到专业名匹配到的所有层次id
def get_level(request):
    majorid = request.POST.get('majorid',None)
    # print(schoolid)
    info = Majors.objects.get(id=majorid)
    info2 = Majors.objects.filter(major_name=info.major_name,is_status=1)
    # print(info2)
    # list = []
    # for item in info2.all():
    #     level = ''
    #     if item.level == 0:
    #         level = '高起专'
    #     elif item.level == 1:
    #         level = '高起本'
    #     elif item.level == 2:
    #         level = '专升本'
    #     list.append([item.level,level])
    # print(list)
    lis = []
    lis2 = []
    for ite in info2.all():  # 按此，是因为，如果几个相同也只会往列表存一个
        if ite.level not in lis:
            lis.append(ite.level)
    # print(lis)
    for i in lis:
        level = ''
        if i == 0:
            level = '高起专'
        elif i == 1:
            level = '高起本'
        elif i == 2:
            level = '专升本'
        lis2.append(level)
    # print(lis2)
    # 接下来就是把列表合并为一个，就可
    listsss = []
    lists = list(zip(lis, lis2))
    for item in lists:
        listsss.append([item[0], item[1]])
    print(listsss)
    return JsonResponse({'data':listsss})

#获取院校信息，先获取层次值，在获取上一步已经选择的专业名称的id；通过获取的专业名称和层次值来找院校
def get_schools(request):
    levelid = request.POST.get('levelid',None)
    maj = request.POST.get('maj',None)
    # print(levelid)
    # print(maj)
    info = Majors.objects.get(id=maj)
    # print(info)
    info2 = Majors.objects.filter(major_name=info.major_name,level=levelid,is_status=1)
    # print(info2)
    list = []
    for item in info2.all():
        list.append([item.school_id,item.school.name])
    return JsonResponse({'data':list})
    # return HttpResponse(123)

#添加报名信息:上传数据，除电话外，所有的都是必填的或默认,选专业这四处如果不填，不会跳转，需要写提示。。。
def addssOrd(request):
    real_name = request.POST.get('real_name')
    idcard=request.POST.get('idcard')
    phone = request.POST.get('phone',None)
    user = request.POST.get('user')
    major_cates=request.POST.get('major_cates',None)
    major=request.POST.get('major',None)
    order_level=request.POST.get('order_level',None)    #实际取到的值是0/1/2，并不能传入
    order_school=request.POST.get('order_school',None)
    status=request.POST.get('status',None)

    #专业id获取名称，通过名称和输入框传来的层次值（精确些还需要筛选order_school这个条件），查找到专业的id及其层次id
    mjid = Majors.objects.get(id=major)
    # print(mjid.major_name)
    ord_level=Majors.objects.get(major_name=mjid.major_name,level=order_level,school_id=order_school)
    # print(ord_level.id)
    #判断用户id是否存在，并判断用户账户状态为1的,此次并没有写用户名不可重复
    info = Users.objects.filter(id=user,is_status=1).exists()
    # print(info)
    if info or major_cates is not None or major is not None or order_school is not None or ord_level is not None:
        Orders.objects.create(
            real_name=real_name,
            idcard=idcard,
            phone=phone,
            user_id=user,
            major_cates_id=major_cates,
            major_id=major,
            order_level_id=ord_level.id,
            order_school_id=order_school,
            status=status,
        )
        return JsonResponse({
            'status': 'success',
            'message': '创建成功',
            'info': ''
        })
    return JsonResponse({
        'status': 'fail',
        'message': '用户id不存在！',
        'info': ''
    })

#删除报名信息，其实是把status变为0
def delOrd(request):
    ord_id=request.GET.get('ord_id')
    order = Orders.objects.get(id=ord_id)
    context={'ord':ord}
    is_status = 0
    order.is_status = is_status
    order.save()
    return render(request, 'order/order_list.html', context=context)

#已删除报名信息展示
def deldOrd(request):
    order = Orders.objects.filter(is_status=0)
    context ={'order':order}
    return render(request,'order/deld_ord.html',context=context)

#还原已删除报名信息
def ordOrd(request):
    #判断当前id是否存在
    ord_id = request.GET.get('ord_id', None)
    order = Orders.objects.get(id=ord_id)  # 获取所有选中id的信息
    context = {
        'order': order,
    }
    is_status = 1
    order.is_status = is_status
    order.save()
    return render(request,'order/deld_ord.html',context=context)

#永久删除报名信息，删除存在数据库的信息
def delesOrd(request):
    #获取id
    ord_id = request.GET.get('ord_id', None)
    order = Orders.objects.get(id=ord_id)  # 获取所有选中id的信息
    context = {
        'order': order,
    }
    Orders.objects.get(id=ord_id).delete()
    return render(request,'order/deld_ord.html',context=context)
