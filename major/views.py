from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import JsonResponse
from school.models import Schools
from .models import Majors,MajorCates

# Create your views here.
#专业列表展示
def majorList(request):
    major = Majors.objects.filter(is_status=1)
    context ={'major':major}
    return render(request,'major/major_list.html',context=context)

#查看专业详情
def detailMaj(request):
    maj_id = request.POST.get('maj_id',None)
    major = Majors.objects.get(id=maj_id)
    return render(request,'major/detailmaj.html',context={'major':major})

#编辑专业详情:接收数据
def editMaj(request):
    maj_id = request.GET.get('maj_id',None)
    major = Majors.objects.get(id=maj_id)
    school = Schools.objects.filter(is_status=1).exclude(name=major.school.name)
    major_cates = MajorCates.objects.filter(is_status=1).exclude(catename=major.major_category.catename)
    context = {
        'major':major,
        'major_cates':major_cates,
        'school':school
    }
    return render(request,'major/edit_maj.html',context=context)

#编辑专业详情:上传数据
def updateMaj(request):
    # 接收数据
    maj_id = request.POST.get("maj_id", None)
    # '''处理数据'''
    data = request.POST.get('data', None)
    data = json.loads(data)
    # '''对数据进行处理,更新数据库'''
    maj = Majors.objects.filter(id=maj_id)
    maj.update(**data)
    return HttpResponse(123)

#添加专业:获取新页面
def addMaj(request):
    school = Schools.objects.filter(is_status=1)
    major_cates = MajorCates.objects.filter(is_status=1)
    context = {
        'major_cates': major_cates,
        'school': school
    }
    return render(request, 'major/add_maj.html',context=context)

#添加专业:上传数据，除了名称必写之外，其他的可默认或为空的，专业名称可重复
def addssMaj(request):
    major_name = request.POST.get('major_name')
    major_desciption =request.POST.get('major_desciption',None)
    level=request.POST.get('level',None)
    school=request.POST.get('school',None)
    major_category=request.POST.get('major_category',None)
    is_recommend=request.POST.get('is_recommend',None)
    times = request.POST.get('times',None)    #学制的数据类型是浮点数，如果为空会报错
    is_fast=request.POST.get('is_fast',None)
    is_special=request.POST.get('is_special',None)
    detail=request.POST.get('detail',None)
    Majors.objects.create(
        major_name=major_name,
        major_desciption=major_desciption,
        level=level,
        major_category_id=major_category,
        school_id=school,
        is_recommend=is_recommend,
        times= 0.0 if times==''else times,
        is_fast=is_fast,
        is_special=is_special,
        detail=detail
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#删除专业信息，其实是把status变为0
def delMaj(request):
    #判断当前id是否存在
    maj_id = request.GET.get('maj_id', None)
    major = Majors.objects.get(id=maj_id)  #获取所有选中id的信息
    context = {
        'major':major,
    }
    is_status = 0
    major.is_status = is_status
    major.save()
    return render(request,'major/major_list.html',context=context)


#专业分类展示，父分类这个怎么展示，关系到编辑和添加
def majorCates(request):
    major_cates = MajorCates.objects.filter(is_status=1)
    context ={'major_cates':major_cates}
    return render(request,'major/major_cates.html',context=context)

#删除专业分类，其实是把status变为0
def delCates(request):
    #判断当前id是否存在
    cates_id = request.GET.get('cates_id', None)
    major_cates = MajorCates.objects.get(id=cates_id)  #获取所有选中id的信息
    context = {
        'major_cates':major_cates,
    }
    is_status = 0
    major_cates.is_status = is_status
    major_cates.save()
    return render(request,'major/major_cates.html',context=context)

#添加专业分类:获取新页面
def addCates(request):
    return render(request, 'major/add_cates.html')

#添加新专业分类：上传数据，名称不允许为空，不允许重复
def addssCates(request):
    catename = request.POST.get('catename')
    # 判断是否存在
    info = MajorCates.objects.filter(catename=catename).exists()
    if info:  # 如果为true，控制台返回值
        return JsonResponse({
            'status': 'fail',
            'message': '当前专业分类已存在',#在html写了框，没有用到这个
            'tagid': 'catename'
        })
    # 如果不存在就增加数据
    MajorCates.objects.create(
        catename=catename,
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#编辑专业分类:接收数据
def editCates(request):
    cates_id = request.GET.get('cates_id',None)
    major_cates = MajorCates.objects.get(id=cates_id)
    context = {
        'major_cates':major_cates,
    }
    return render(request,'major/edit_cates.html',context=context)

#编辑专业分类:上传数据,此处并没有考虑更改后重复的问题,没有写pid，则编辑名称不影响它
def updateCates(request):
    # 接收数据
    data = request.POST.get('data', None)
    cates_id = request.POST.get("cates_id",None)
    data = json.loads(data)
    major_cates = MajorCates.objects.get(id=cates_id)

    if data['catename'] != '':
        major_cates.catename = data['catename']

    major_cates.save()
    return JsonResponse({
        "status": "success",
        "message": "信息更改成功",
        "info": ""
    })

#已删除专业信息展示
def deldMaj(request):
    major = Majors.objects.filter(is_status=0)
    context = {'major': major}
    return render(request,'major/deld_maj.html',context=context)

#还原已删除专业
def majMaj(request):
    #判断当前id是否存在
    maj_id = request.GET.get('maj_id', None)
    major = Majors.objects.get(id=maj_id)  # 获取所有选中id的信息
    context = {
        'major': major,
    }
    is_status = 1
    major.is_status = is_status
    major.save()
    return render(request,'major/deld_maj.html',context=context)

#永久删除专业信息，删除存在数据库的信息
def delesMaj(request):
    #获取id
    maj_id = request.GET.get('maj_id', None)
    major = Majors.objects.get(id=maj_id)  # 获取所有选中id的信息
    context = {
        'major': major,
    }
    Majors.objects.get(id=maj_id).delete()
    return render(request,'major/deld_maj.html',context=context)

#已删除专业分类展示
def deldCates(request):
    major_cates = MajorCates.objects.filter(is_status=0)
    context ={'major_cates':major_cates}
    return render(request,'major/deld_cates.html',context=context)

#还原已删除专业分类
def catesCates(request):
    #判断当前id是否存在
    cates_id = request.GET.get('cates_id', None)
    major_cates = MajorCates.objects.get(id=cates_id)  # 获取所有选中id的信息
    context = {
        'major_cates': major_cates,
    }
    is_status = 1
    major_cates.is_status = is_status
    major_cates.save()
    return render(request,'major/deld_cates.html',context=context)

#永久删除专业分类，删除存在数据库的信息
def delesCates(request):
    #获取id
    cates_id = request.GET.get('cates_id', None)
    major_cates = MajorCates.objects.get(id=cates_id)  # 获取所有选中id的信息
    context = {
        'major_cates': major_cates,
    }
    MajorCates.objects.get(id=cates_id).delete()
    return render(request,'major/deld_cates.html',context=context)

