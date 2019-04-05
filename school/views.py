from django.shortcuts import render
from .models import Schools,SchoolType,SchoolFeatures
from user.models import Provinces,Citys
import json
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

#院校信息表展示
def schList(request):
    school = Schools.objects.filter(is_status=1)
    context = {
        'school':school
    }
    return render(request,'school/list1.html',context=context)

#编辑院校信息:接收数据
def editSch(request):
    sch_id = request.GET.get('sch_id',None)
    school = Schools.objects.get(id=sch_id)
    province = Provinces.objects.all()
    sch_features = SchoolFeatures.objects.filter(is_status=1)
    sch_type = SchoolType.objects.filter(is_status=1)
    context = {
        'sch_type':sch_type,
        'sch_features':sch_features,
        'province':province,
        'school':school
    }
    return render(request,'school/edit_sch1.html',context=context)

#编辑院校信息:上传数据
#问题在于，不在data的数据，即使不更改，提交后会自动为空或默认值，图片,省份已经写好，剩余的特征，类型，是否911.。。
def updateSch(request):
    # 接收数据
    sch_id = request.POST.get("sch_id",None)
    sch_pro = request.POST.get("sch_pro",None)
    # print(sch_pro)
    sch_city = request.POST.get("sch_city",None)
    # print(sch_city)

    schools = Schools.objects.get(id=sch_id)
    '''处理数据'''
    data = request.POST.get('data',None)
    data = json.loads(data)

    '''处理mtm'''
    school_type = data.pop('school_type')
    school_feature = data.pop('school_feature')

    '''处理省份和市的数据'''
    # print(schools.sch_pro)
    # print(schools.sch_city)
    schools.sch_pro = Provinces.objects.get(provinceid=sch_pro)
    # print(schools.sch_pro)
    schools.sch_city = Citys.objects.get(cityid=sch_city)
    # print(schools.sch_city)


    '''对mtm进行数据存储处理'''
    if school_type != '':
        schools.school_type.clear()
        schools.school_type.add(*school_type)

    if school_feature != '':
        schools.scholl_feature.clear()
        schools.scholl_feature.add(*school_feature)


    '''处理图片数据'''
    # print(schools.banner)
    # print(schools.emblem)
    # print(schools.diploma_images)
    # print(schools.degree_images)
    banner = request.FILES.get("banner")
    emblem = request.FILES.get("emblem")
    diploma = request.FILES.get("diploma")
    degree = request.FILES.get("degree")
    if banner != None:      #none：即没有上传新图片时的banner值
        schools.banner = banner
    print(schools.banner)
    if emblem != None:
        schools.emblem = emblem
    print(schools.emblem)
    if diploma != None:
        schools.diploma_images = diploma
    print(schools.diploma_images)
    if degree != None:
        schools.degree_images = degree
    print(schools.degree_images)
    schools.save()
    '''对其他数据进行处理'''
    sch = Schools.objects.filter(id=sch_id)
    sch.update(**data)

    return HttpResponse(123)

#查看院校详情
def detailSch(request):
    sch_id = request.POST.get('sch_id',None)
    school = Schools.objects.get(id=sch_id)
    return render(request,'school/detailsch.html',context={'school':school})

#删除院校，其实是把status变为0
def delSch(request):
    #判断当前id是否存在
    sch_id = request.GET.get('sch_id', None)
    school = Schools.objects.get(id=sch_id)  #获取所有选中id的信息
    context = {
        'school':school,
    }
    is_status = 0
    school.is_status = is_status
    school.save()
    return render(request,'school/list1.html',context=context)

#添加新院校：获取新页面
def addSch(request):
    return render(request,'school/add_sch.html')

#添加新院校：上传数据，判断输入这里比较简陋，后续优化，按照添加用户的方法来
def addssSch(request):
    name = request.POST.get('name', None)
    description = request.POST.get('description', None)
    is_985 = request.POST.get('is_985',None)
    is_211 = request.POST.get('is_211',None)
    is_double = request.POST.get('is_double',None)

    # 判断院校是否存在,以及不能为空
    info = Schools.objects.filter(name=name).exists()
    # infoo = Schools.objects.filter(name=name)
    # info2 = Schools.objects.filter(description=description)
    # if infoo or info2 == '':
    #     return JsonResponse({
    #         'status': 'fail',
    #         'message': '必填项不允许为空',#两个fail怎么写
    #         'tagid': 'name'
    #     })

    if info:  # 如果为true，控制台返回值
        return JsonResponse({
            'status': 'fail',
            'message': '当前院校已存在',#在html写了框，没有用到这个
            'tagid': 'name'
        })
    # 如果不存在就增加用户数据
    Schools.objects.create(
        name=name,
        description=description,
        is_985=is_985,
        is_211 = is_211,
        is_double = is_double,
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#院校类型表展示
def schType(request):
    school_type = SchoolType.objects.filter(is_status=1)
    context = { 'school_type':school_type }
    return render(request,'school/schtype.html',context=context)

#院校类型表编辑:接收数据
def editType(request):
    type_id = request.GET.get('type_id', None)
    school_type = SchoolType.objects.get(id=type_id)
    context = {'school_type': school_type}
    return render(request, 'school/edit_type.html', context=context)

#院校类型表编辑:上传数据
def updateType(request):
    # 接收数据
    data = request.POST.get('data', None)
    typeid = request.POST.get("type_id",None)
    data = json.loads(data)
    school_type = SchoolType.objects.get(id=typeid)

    if data['type_name'] != '':
        school_type.type_name = data['type_name']

    if data['notes'] != '':
        school_type.notes = data['notes']
    school_type.save()
    return JsonResponse({
        "status": "success",
        "message": "院校类型信息更改成功",
        "info": ""
    })

#删除院校类型，其实是把status变为0
def delType(request):
    #判断当前id是否存在
    type_id = request.GET.get('type_id', None)
    school_type = SchoolType.objects.get(id=type_id)  #获取所有选中id的信息
    context = {'school_type': school_type}
    is_status = 0
    school_type.is_status = is_status
    school_type.save()
    return render(request,'school/schtype.html',context=context)

#添加新院校类型：获取新页面
def addSchtype(request):
    return render(request,'school/add_schtype.html')

#添加新院校类型：上传数据，没有给输入限定过多条件
def addssSchtype(request):
    type_name = request.POST.get('type_name', None)
    notes = request.POST.get('notes', None)

    # 判断是否存在，此次直接写了一个空值在数据表中，使后面再添加都不能为空
    info = SchoolType.objects.filter(type_name=type_name).exists()
    if info:  # 如果为true，控制台返回值
        return JsonResponse({
            'status': 'fail',
            'message': '当前院校类型已存在',#在html写了框，没有用到这个
            'tagid': 'type_name'
        })
    # 如果不存在就增加用户数据
    SchoolType.objects.create(
        type_name = type_name,
        notes=notes
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#院校特征表展示
def schFea(request):
    school_fea = SchoolFeatures.objects.filter(is_status=1)
    context = { 'school_fea':school_fea}
    return render(request,'school/schfea.html',context=context)

#院校特征表编辑:接收数据
def editFea(request):
    fea_id = request.GET.get('fea_id', None)
    school_fea = SchoolFeatures.objects.get(id=fea_id)
    context = {'school_fea': school_fea}
    return render(request, 'school/edit_fea.html', context=context)

#院校特征表编辑:上传数据
def updateFea(request):
    # 接收数据
    data = request.POST.get('data', None)
    feaid = request.POST.get("fea_id",None)
    data = json.loads(data)
    school_fea = SchoolFeatures.objects.get(id=feaid)

    if data['feature_name'] != '':
        school_fea.feature_name = data['feature_name']

    if data['notes'] != '':
        school_fea.notes = data['notes']
    school_fea.save()
    return JsonResponse({
        "status": "success",
        "message": "院校特征信息更改成功",
        "info": ""
    })

#删除院校特征，其实是把status变为0
def delFea(request):
    #判断当前id是否存在
    fea_id = request.GET.get('fea_id', None)
    school_fea = SchoolFeatures.objects.get(id=fea_id)
    context = {'school_fea': school_fea}
    is_status = 0
    school_fea.is_status = is_status
    school_fea.save()
    return render(request,'school/schfea.html',context=context)

#添加新院校特征：获取新页面
def addSchfea(request):
    return render(request,'school/add_schfea.html')

#添加新院校特征：上传数据，没有给输入限定过多条件
def addssSchfea(request):
    fea_name = request.POST.get('fea_name', None)
    notes = request.POST.get('notes', None)

    # 判断是否存在，此次直接写了一个空值在数据表中，使后面在添加都不能为空
    info = SchoolFeatures.objects.filter(feature_name=fea_name).exists()
    if info:  # 如果为true，控制台返回值
        return JsonResponse({
            'status': 'fail',
            'message': '当前院校特征已存在',#在html写了框，没有用到这个
            'tagid': 'type_name'
        })
    # 如果不存在就增加
    SchoolFeatures.objects.create(
        feature_name=fea_name,
        notes=notes
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#已删除院校列表展示
def deldSch(request):
    school = Schools.objects.filter(is_status=0)
    context = {'school': school}
    return render(request, 'school/deld_sch.html', context=context)

#还原已删除院校
def schSch(request):
    #判断当前id是否存在
    sch_id = request.GET.get('sch_id', None)
    school = Schools.objects.get(id=sch_id)  # 获取所有选中id的信息
    context = {
        'school': school,
    }
    is_status = 1
    school.is_status = is_status
    school.save()
    return render(request,'school/deld_sch.html',context=context)

#永久删除院校，删除存在数据库的信息,多对多两个表的信息也删除了
def delesSch(request):
    #获取id
    sch_id = request.GET.get('sch_id', None)
    school = Schools.objects.get(id=sch_id)  # 获取所有选中id的信息
    context = {
        'school': school,
    }
    Schools.objects.get(id=sch_id).delete()
    return render(request,'school/deld_sch.html',context=context)


#已删除院校类型表展示
def deldSchtype(request):
    school_type = SchoolType.objects.filter(is_status=0)
    context = {'school_type': school_type}
    return render(request, 'school/deld_schtype.html', context=context)

#还原已删除院校类型，其实是把status变为0
def typeType(request):
    #判断当前id是否存在
    type_id = request.GET.get('type_id', None)
    school_type = SchoolType.objects.get(id=type_id)  #获取所有选中id的信息
    context = {'school_type': school_type}
    is_status = 1
    school_type.is_status = is_status
    school_type.save()
    return render(request,'school/deld_schtype.html',context=context)

#永久删除院校类型，删除存在数据库的信息
def delesType(request):
    #获取id
    type_id = request.GET.get('type_id', None)
    school_type = SchoolType.objects.get(id=type_id)  # 获取所有选中id的信息
    context = {'school_type': school_type}
    SchoolType.objects.get(id=type_id).delete()
    return render(request,'school/deld_schtype.html',context=context)

#已删除院校特征表展示
def deldSchfea(request):
    school_fea = SchoolFeatures.objects.filter(is_status=0)
    context = {'school_fea': school_fea}
    return render(request, 'school/deld_schfea.html', context=context)

#还原已删除院校特征，其实是把status变为1
def feaFea(request):
    #判断当前id是否存在
    fea_id = request.GET.get('fea_id', None)
    school_fea = SchoolFeatures.objects.get(id=fea_id)
    context = {'school_fea': school_fea}
    is_status = 1
    school_fea.is_status = is_status
    school_fea.save()
    return render(request,'school/deld_schfea.html',context=context)

#永久删除院校特征，删除存在数据库的信息
def delesFea(request):
    #获取id
    fea_id = request.GET.get('fea_id', None)
    school_fea = SchoolFeatures.objects.get(id=fea_id)
    context = {'school_fea': school_fea}
    SchoolFeatures.objects.get(id=fea_id).delete()
    return render(request,'school/deld_schfea.html',context=context)


