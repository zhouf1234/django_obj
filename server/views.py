from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import JsonResponse
from .models import ServerCategorys,ServerPosts,Keywords,Aquestions,Attachments,Centers
from school.models import Schools
from major.models import Majors

# Create your views here.
#服务中心文章列表展示
def serverpostsList(request):
    server_post =ServerPosts .objects.filter(is_status=1)
    context ={'server_post':server_post}
    return render(request,'server/server_posts_list.html',context=context)

#查看服务文章详情
def detailserPos(request):
    ser_pos_id = request.POST.get('ser_pos_id',None)
    ser_posts = ServerPosts.objects.get(id=ser_pos_id)
    return render(request,'server/detail_ser_pos.html',context={'ser_posts':ser_posts})

#添加新服务文章:获取新页面
def addserPos(request):
    ques_school = Schools.objects.filter(is_status=1)
    cateid=ServerCategorys.objects.filter(is_status=1)
    keywords=Keywords.objects.all()
    context = {
        'ques_school': ques_school,
        'cateid': cateid,
        'keywords':keywords
    }
    return render(request, 'server/add_ser_pos.html',context=context)

#添加新服务文章，上传数据，除了标题外，都可不填
def addssserPos(request):
    #获取data的数据
    data = request.POST.get('data', None)
    data = json.loads(data)
    # print(data['post_school'])
    # 判断文章标题是否存在
    info = ServerPosts.objects.filter(post_title=data['post_title'], is_status=1).exists()
    if info:
        return JsonResponse({
            'status': 'fail',
            'message': '该服务文章已存在！',
            'info': ''
        })
    ServerPosts.objects.create(
        post_title=data['post_title'],
        source='舟炬教育' if data['source']=='' else data['source'],
        source_link='http://www.zhoujuedu.com' if data['source_link']=='' else data['source_link'],
        #这几项是外键的id如果不填，会报错，都给个默认值id吧
        #但是major的外键id不填却可以，什么原因呢
        cateid_id='1' if data['cateid']==' ' else data['cateid'],
        keywords_id='8' if data['keywords']==' ' else data['keywords'],
        server_post_school_id='11' if data['server_post_school']==' ' else data['server_post_school'],
        post_content=data['post_content'],
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#删除服务文章，其实是把status变为0
def delserPos(request):
    ser_pos_id=request.GET.get('ser_pos_id')
    ser_posts = ServerPosts.objects.get(id=ser_pos_id)
    context={'ser_posts':ser_posts}
    is_status = 0
    ser_posts.is_status = is_status
    ser_posts.save()
    return render(request, 'server/server_posts_list.html', context=context)

#编辑服务文章:接收数据
def editserPos(request):
    ser_pos_id = request.GET.get('ser_pos_id',None)
    ser_posts = ServerPosts.objects.get(id=ser_pos_id)
    ser_school = Schools.objects.filter(is_status=1).exclude(name=ser_posts.server_post_school.name)
    cateid = ServerCategorys.objects.filter(is_status=1).exclude(server_name=ser_posts.cateid.server_name)
    keywords = Keywords.objects.exclude(key_name=ser_posts.keywords.key_name)
    context = {
        'ser_posts':ser_posts,
        'ser_school':ser_school,
        'cateid':cateid,
        'keywords':keywords
    }
    return render(request,'server/edit_ser_pos.html',context=context)

#编辑服务文章:上传数据
def updateserPos(request):
    # 接收数据
    ser_pos_id = request.POST.get("ser_pos_id",None)

    '''处理数据'''
    data = request.POST.get('data',None)
    data = json.loads(data)

    '''对数据进行处理'''
    pos = ServerPosts.objects.filter(id=ser_pos_id)
    pos.update(**data)

    return HttpResponse(123)

#服务中心分类展示
def serverCates(request):
    server_cates =ServerCategorys .objects.filter(is_status=1)
    context ={'server_cates':server_cates}
    return render(request,'server/server_cates.html',context=context)

#添加服务中心分类:获取新页面
def addserCates(request):
    return render(request, 'server/add_ser_cates.html')

#添加新服务分类：上传数据，名称不允许为空，不允许重复
def addssserCates(request):
    server_name = request.POST.get('server_name')
    # 判断是否存在
    info = ServerCategorys.objects.filter(server_name=server_name).exists()
    if info:  # 如果为true，控制台返回值
        return JsonResponse({
            'status': 'fail',
            'message': '当前分类已存在',#在html写了框，没有用到这个
            'tagid': 'server_name'
        })
    # 如果不存在就增加数据
    ServerCategorys.objects.create(
        server_name=server_name,
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#删除服务分类，其实是把status变为0
def delserCates(request):
    ser_cates_id=request.GET.get('ser_cates_id')
    ser_cates = ServerCategorys.objects.get(id=ser_cates_id)
    context={'ser_cates':ser_cates}
    is_status = 0
    ser_cates.is_status = is_status
    ser_cates.save()
    return render(request, 'server/server_cates.html', context=context)

#编辑服务分类:接收数据
def editserCates(request):
    ser_cates_id = request.GET.get('ser_cates_id',None)
    ser_cates = ServerCategorys.objects.get(id=ser_cates_id)
    context = {
        'ser_cates':ser_cates,
    }
    return render(request,'server/edit_ser_cates.html',context=context)

#编辑服务分类:上传数据
def updateserCates(request):
    # 接收数据
    data = request.POST.get('data', None)
    ser_cateid = request.POST.get("ser_cateid",None)
    data = json.loads(data)
    ser_cates = ServerCategorys.objects.get(id=ser_cateid)

    if data['server_name'] != '':
        ser_cates.server_name = data['server_name']
    ser_cates.save()
    return JsonResponse({
        "status": "success",
        "message": "更改成功",
        "info": ""
    })

#教学中心列表展示
def servercenterList(request):
    center =Centers .objects.filter(is_status=1)
    context ={'center':center}
    return render(request,'server/server_center_list.html',context=context)

#查看教学中心详情
def detailserCenter(request):
    ser_cen_id = request.POST.get('ser_cen_id',None)
    ser_center = Centers.objects.get(id=ser_cen_id)
    return render(request,'server/detail_ser_center.html',context={'ser_center':ser_center})

#添加教学中心:获取新页面
def addserCenter(request):
    return render(request, 'server/add_ser_center.html')

#添加教学中心:上传数据,名称和编号不能为空
def addssserCenter(request):
    cen_name = request.POST.get('cen_name')
    cen_num=request.POST.get('cen_num')
    address = request.POST.get('address',None)
    phone = request.POST.get('phone',None)
    is_direct=request.POST.get('is_direct',None)
    #判断教学中心名称或编号是否存在
    info = Centers.objects.filter(cen_name=cen_name,is_status=1).exists()
    info2 = Centers.objects.filter(cen_num=cen_num,is_status=1).exists()
    # print(info)
    if info or info2:
        return JsonResponse({
            'status': 'fail',
            'message': '教学中心或编号已存在！',#在html写了框，没有用到这个
            'info': ''
        })
    Centers.objects.create(
        cen_name=cen_name,
        cen_num=cen_num,    #因为字段是int，导致如果为空会报错
        address=address,
        phone=phone,
        is_direct=is_direct,
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#删除教学中心，其实是把status变为0
def delserCenter(request):
    ser_center_id=request.GET.get('ser_center_id')
    ser_center = Centers.objects.get(id=ser_center_id)
    context={'ser_center':ser_center}
    is_status = 0
    ser_center.is_status = is_status
    ser_center.save()
    return render(request, 'server/server_center_list.html', context=context)

#编辑教学中心:接收数据
def editserCenter(request):
    ser_center_id = request.GET.get('ser_center_id',None)
    ser_center = Centers.objects.get(id=ser_center_id)
    context = {
        'ser_center':ser_center,
    }
    return render(request,'server/edit_ser_center.html',context=context)

#编辑教学中心:上传数据
def updateserCenter(request):
    # 接收数据
    ser_center_id = request.POST.get("ser_center_id",None)

    '''处理数据'''
    data = request.POST.get('data',None)
    data = json.loads(data)

    '''对数据进行处理'''
    cen = Centers.objects.filter(id=ser_center_id)
    cen.update(**data)

    return HttpResponse(123)

#附件表展示
def serverAtta(request):
    atta =Attachments .objects.filter(is_status=1)
    context ={'atta':atta}
    return render(request,'server/server_atta.html',context=context)

#查看附件详情
def detailserAtta(request):
    ser_atta_id = request.POST.get('ser_atta_id',None)
    ser_atta = Attachments.objects.get(id=ser_atta_id)
    return render(request,'server/detail_ser_atta.html',context={'ser_atta':ser_atta})

#添加附件:获取新页面
def addserAtta(request):
    return render(request, 'server/add_ser_atta.html')

#添加附件:上传数据,都不能为空
def addssserAtta(request):
    atta_name = request.POST.get('atta_name')
    filename=request.POST.get('filename')
    #判断是否存在
    info = Attachments.objects.filter(atta_name=atta_name,filename=filename).exists()
    # print(info)
    if info:
        return JsonResponse({
            'status': 'fail',
            'message': '附件已存在！',#在html写了框，没有用到这个
            'info': ''
        })
    Attachments.objects.create(
        atta_name=atta_name,
        filename=filename,
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#删除附件，其实是把status变为0
def delserAtta(request):
    ser_atta_id=request.GET.get('ser_atta_id')
    ser_atta = Attachments.objects.get(id=ser_atta_id)
    context={'ser_atta':ser_atta}
    is_status = 0
    ser_atta.is_status = is_status
    ser_atta.save()
    return render(request, 'server/server_atta.html', context=context)

#编辑附件:接收数据
def editserAtta(request):
    ser_atta_id = request.GET.get('ser_atta_id',None)
    ser_atta = Attachments.objects.get(id=ser_atta_id)
    context = {
        'ser_atta':ser_atta,
    }
    return render(request,'server/edit_ser_atta.html',context=context)

#编辑附件:上传数据
def updateserAtta(request):
    # 接收数据
    data = request.POST.get('data', None)
    ser_attaid = request.POST.get("ser_attaid",None)
    data = json.loads(data)
    ser_atta = Attachments.objects.get(id=ser_attaid)

    if data['atta_name'] != '':
        ser_atta.atta_name = data['atta_name']
    if data['filename'] != '':
        ser_atta.filename = data['filename']
    ser_atta.save()
    return JsonResponse({
        "status": "success",
        "message": "更改成功",
        "info": ""
    })

#模拟题表展示
def serverAques(request):
    aques =Aquestions .objects.filter(is_status=1)
    context ={'aques':aques}
    return render(request,'server/server_aques.html',context=context)

#查看模拟题附件详情
def detailserAqu(request):
    ser_aqu_id = request.POST.get('ser_aqu_id',None)
    ser_aqu = Aquestions.objects.get(id=ser_aqu_id)
    return render(request,'server/detail_ser_aqu.html',context={'ser_aqu':ser_aqu})

#添加新模拟题:获取新页面,五项都不允许为空
def addserAqu(request):
    que_school = Schools.objects.filter(is_status=1)
    context = {
        'ques_school': que_school,
    }
    return render(request, 'server/add_ser_aqu.html',context=context)

#获取院校id，反向获取到专业信息表的所有院校对应专业id（无重复名称的）
def get_maj(request):
    schid = request.POST.get('schid',None)
    info = Majors.objects.filter(school_id=schid,is_status=1)
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

#通过专业列表的id，得到专业名，再得到专业名和院校id匹配到的所有层次
def get_lev(request):
    majid = request.POST.get('majid',None)
    school =request.POST.get('school',None)
    # print(school)
    info = Majors.objects.get(id=majid)
    info2 = Majors.objects.filter(major_name=info.major_name,school_id=school,is_status=1)
    # print(info2)
    list = []
    for item in info2.all():
        level = ''
        if item.level == 0:
            level = '高起专'
        elif item.level == 1:
            level = '高起本'
        elif item.level == 2:
            level = '专升本'
        list.append([item.level, level])
    return JsonResponse({'data': list})

#添加模拟题:上传数据,都不能为空
def addssserAqu(request):
    ques_name = request.POST.get('ques_name')
    ques_filename=request.POST.get('ques_filename')
    ques_school = request.POST.get('ques_school')
    ques_major = request.POST.get('ques_major')
    ques_level = request.POST.get('ques_level')  #实际取到的值是0/1/2，并不能传入

    #判断是否存在
    info = Aquestions.objects.filter(ques_name=ques_name,ques_filename=ques_filename,is_status=1).exists()
    # print(info)
    if info or ques_school==' ' or ques_major==' ' or ques_level==' ':
        return JsonResponse({
            'status': 'fail',
            'message': '模拟题已存在或必填项未填写！',#在html写了框，没有用到这个
            'info': ''
        })
    # 专业id获取名称，通过名称和输入框传来的层次值（精确些还需要筛选order_school这个条件），查找到专业的id及其层次id
    mjid = Majors.objects.get(id=ques_major)
    qu_level=Majors.objects.get(major_name=mjid.major_name,level=ques_level,school_id=ques_school)
    # print(qu_level.id,qu_level.major_name)
    Aquestions.objects.create(
        ques_name=ques_name,
        ques_filename=ques_filename,
        ques_school_id=ques_school,
        ques_major_id=ques_major,
        ques_level_id=qu_level.id
    )
    return JsonResponse({
        'status': 'success',
        'message': '创建成功',
        'info': ''
    })

#删除模拟题，其实是把status变为0
def delserAqu(request):
    ser_aqu_id=request.GET.get('ser_aqu_id')
    ser_aqu = Aquestions.objects.get(id=ser_aqu_id)
    context={'ser_aqu':ser_aqu}
    is_status = 0
    ser_aqu.is_status = is_status
    ser_aqu.save()
    return render(request, 'server/server_aques.html', context=context)

#编辑模拟题附件:接收数据
#相同学校，相同专业名，不同层次，使之只显示一次专业名
def editserAqu(request):
    ser_aqu_id = request.GET.get('ser_aqu_id',None)
    ser_aqu = Aquestions.objects.get(id=ser_aqu_id)
    #下拉出的学校和专业列表，不包含is_status=0的，和当前这条数据的学校名和专业名
    ques_school = Schools.objects.filter(is_status=1).exclude(name=ser_aqu.ques_school.name)
    ques_major = Majors.objects.filter(is_status=1).exclude(major_name =ser_aqu.ques_major.major_name)
    majors = Majors.objects.filter(major_name=ser_aqu.ques_major.major_name,school_id=ser_aqu.ques_school.id,is_status=1).exclude(level=ser_aqu.ques_level.level)
    q_mj = Majors.objects.values('major_name').distinct().filter(is_status=1).exclude(major_name =ser_aqu.ques_major.major_name)
    q_mj_lis = []
    for i in q_mj:
        # print(i['major_name'])  #再通过名字和school_id取到符合条件的第一个
        q_mj2 = Majors.objects.filter(major_name=i['major_name'],school_id=ser_aqu.ques_school.id).first()
        if q_mj2 !=None:
            q_mj_lis.append(q_mj2)
    # print(q_mj_lis)
    context = {
        'ser_aqu':ser_aqu,
        'ques_school':ques_school,
        'ques_major':ques_major,
        'q_mj_lis':q_mj_lis,
        'majors':majors,
    }
    return render(request,'server/edit_ser_aqu.html',context=context)

#编辑模拟题附件：上传数据
def updateserAqu(request):
    # 获取数据
    data = request.POST.get('data', None)
    ser_aquid = request.POST.get('ser_aquid', None)

    data = json.loads(data)
    aqu = Aquestions.objects.get(id=ser_aquid)
    if data['ques_school'] != '':
        aqu.ques_school = Schools.objects.get(id=data['ques_school'])
        if data['ques_major'] != '':
            aqu.ques_major = Majors.objects.get(id=data['ques_major'])
            if data['ques_level'] !='':
                #data['ques_level']得到的值其实是0/1/2
                # print(mj.major_name)
                # print(data['ques_level'])
                mj =Majors.objects.get(id=data['ques_major'])
                aqu.ques_level = Majors.objects.get(major_name=mj.major_name,level=data['ques_level'],school_id=data['ques_school'])
                # print(aqu.ques_level)

    if data['ques_name'] != '':
        aqu.ques_name = data['ques_name']

    if data['ques_filename'] != '':
        aqu.ques_filename = data['ques_filename']

    aqu.save()
    return JsonResponse({
        "status": "success",
        "message": "信息更改成功",
        "info": ""
    })

#已删除服务中心文章列表展示
def deldserPos(request):
    server_post =ServerPosts .objects.filter(is_status=0)
    context ={'server_post':server_post}
    return render(request,'server/deld_ser_pos.html',context=context)

#已删除服务中心分类展示
def deldserCates(request):
    server_cates =ServerCategorys .objects.filter(is_status=0)
    context ={'server_cates':server_cates}
    return render(request,'server/deld_ser_cates.html',context=context)

#已删除教学中心列表展示
def deldserCenter(request):
    center =Centers .objects.filter(is_status=0)
    context ={'center':center}
    return render(request,'server/deld_ser_center.html',context=context)

#已删除附件表展示
def deldserAtta(request):
    atta =Attachments .objects.filter(is_status=0)
    context ={'atta':atta}
    return render(request,'server/deld_ser_atta.html',context=context)

#已删除模拟题表展示
def deldserAqu(request):
    aques =Aquestions .objects.filter(is_status=0)
    context ={'aques':aques}
    return render(request,'server/deld_ser_aqu.html',context=context)

#还原服务文章，其实是把status变为1
def posserPos(request):
    ser_pos_id=request.GET.get('ser_pos_id')
    ser_posts = ServerPosts.objects.get(id=ser_pos_id)
    context={'ser_posts':ser_posts}
    is_status = 1
    ser_posts.is_status = is_status
    ser_posts.save()
    return render(request, 'server/deld_ser_pos.html', context=context)

#还原服务分类，其实是把status变为1
def catesserCates(request):
    ser_cates_id=request.GET.get('ser_cates_id')
    ser_cates = ServerCategorys.objects.get(id=ser_cates_id)
    context={'ser_cates':ser_cates}
    is_status = 1
    ser_cates.is_status = is_status
    ser_cates.save()
    return render(request, 'server/deld_ser_cates.html', context=context)

#还原教学中心，其实是把status变为1
def centerserCenter(request):
    ser_center_id=request.GET.get('ser_center_id')
    ser_center = Centers.objects.get(id=ser_center_id)
    context={'ser_center':ser_center}
    is_status = 1
    ser_center.is_status = is_status
    ser_center.save()
    return render(request, 'server/deld_ser_center.html', context=context)

#还原附件，其实是把status变为1
def attaserAtta(request):
    ser_atta_id=request.GET.get('ser_atta_id')
    ser_atta = Attachments.objects.get(id=ser_atta_id)
    context={'ser_atta':ser_atta}
    is_status = 1
    ser_atta.is_status = is_status
    ser_atta.save()
    return render(request, 'server/deld_ser_atta.html', context=context)

#还原模拟题，其实是把status变为1
def aquserAqu(request):
    ser_aqu_id=request.GET.get('ser_aqu_id')
    ser_aqu = Aquestions.objects.get(id=ser_aqu_id)
    context={'ser_aqu':ser_aqu}
    is_status = 1
    ser_aqu.is_status = is_status
    ser_aqu.save()
    return render(request, 'server/deld_ser_aqu.html', context=context)

#永久删除服务文章，删除存在数据库的信息
def delesserPos(request):
    #获取id
    ser_pos_id = request.GET.get('ser_pos_id')
    ser_posts = ServerPosts.objects.get(id=ser_pos_id)
    context = {'ser_posts': ser_posts}
    ServerPosts.objects.get(id=ser_pos_id).delete()
    return render(request,'server/deld_ser_pos.html',context=context)

#永久删除服务分类，删除存在数据库的信息
def delesserCates(request):
    #获取id
    ser_cates_id = request.GET.get('ser_cates_id')
    ser_cates = ServerCategorys.objects.get(id=ser_cates_id)
    context = {'ser_cates': ser_cates}
    ServerCategorys.objects.get(id=ser_cates_id).delete()
    return render(request,'server/deld_ser_cates.html',context=context)

#永久删除教学中心，删除存在数据库的信息
def delesserCenter(request):
    #获取id
    ser_center_id = request.GET.get('ser_center_id')
    ser_center = Centers.objects.get(id=ser_center_id)
    context = {'ser_center': ser_center}
    Centers.objects.get(id=ser_center_id).delete()
    return render(request,'server/deld_ser_center.html',context=context)

#永久删除附件，删除存在数据库的信息
def delesserAtta(request):
    #获取id
    ser_atta_id = request.GET.get('ser_atta_id')
    ser_atta = Attachments.objects.get(id=ser_atta_id)
    context = {'ser_atta': ser_atta}
    Attachments.objects.get(id=ser_atta_id).delete()
    return render(request,'server/deld_ser_atta.html',context=context)

#永久删除模拟题附件，删除存在数据库的信息
def delesserAqu(request):
    #获取id
    ser_aqu_id = request.GET.get('ser_aqu_id')
    ser_aqu = Aquestions.objects.get(id=ser_aqu_id)
    context = {'ser_aqu': ser_aqu}
    Aquestions.objects.get(id=ser_aqu_id).delete()
    return render(request,'server/deld_ser_aqu.html',context=context)

