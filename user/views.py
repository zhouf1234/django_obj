from django.shortcuts import render,HttpResponse
from .models import Users,Provinces,Citys,Areas,EmailVerifyRecord
from cms.models import Admins
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from cms.check import Base
import json
from utils import email_send

#用户列表展示，is_status=1代表可用，为true
def indexView(request):
    users = Users.objects.filter(is_status=1)
    context = {'users':users}
    return render(request, 'user/user_index1.html', context=context)
    # return render(request,'user/user_index.html',context=context)


#添加用户
class AddUserView(View):
    def get(self,request):
        return render(request,'user/adduser1.html')

    def post(self,request):
        nickname = request.POST.get('nickname',None)
        #判断用户是否存在
        info = Users.objects.filter(nickname=nickname).exists()
        if info:    #如果为true，控制台返回值
            return JsonResponse({
                'status':'fail',
                'message':'当前用户已存在',
                'tagid':'nickname'
            })
        #如果不存在就增加用户数据
        Users.objects.create(
            nickname=nickname,
            password=make_password(request.POST.get('password',None)), #密码加密处理
            email=request.POST.get('email',None),
            reg_ip = Base.get_ip(request),
            reg_time=Base.getNowTime(request)
        )
        return JsonResponse({
            'status': 'success',
            'message': '创建成功',
            'info': ''
        })

#编辑用户信息
class EditUser(View):
    def get(self,request):
        #判断当前id是否存在
        user_id = request.GET.get('user_id',None)   #此处获取的'user_id'是用户列表html的function edit_user(temp)设置获取的
        info = Users.objects.filter(id=user_id)
        if info:
            users = Users.objects.get(id = user_id)  #获取所有选中id的信息
            province = Provinces.objects.all()      #获取所有省份信息
            context = {
                'users':users,
                'provinces':province
            }
            return render(request,'user/edituser1.html',context=context)

#获取市县信息
def get_city(request):
    proid = request.POST.get('proid',None)
    info = Citys.objects.filter(provinceid=proid)
    list = []
    for item in info.all():
        list.append([item.cityid,item.city])
    return JsonResponse({'data':list})      #data对应的就是edituder.html的function have_city(temp)下方的info.data

def get_country(request):
    cityid = request.POST.get('cityid',None)
    info = Areas.objects.filter(cityid=cityid)
    list = []
    for item in info.all():
        list.append([item.areaid,item.area])
    return JsonResponse({'data':list})


def userInfo(request):
    # 获取数据
    data = request.POST.get('data', None)
    userid = request.POST.get('user_id', None)

    data = json.loads(data)

    users = Users.objects.get(pk=userid)
    if data['province'] != '':
        users.province = Provinces.objects.get(provinceid=data['province'])
        if data['city'] != '':
            users.city = Citys.objects.get(cityid=data['city'])
            if data['country'] !='':
                users.country = Areas.objects.get(areaid=data['country'])


    if data['nickname'] != '':
        users.nickname = data['nickname']

    if data['phone'] != '':
        users.phone = data['phone']

    if data['id_name'] != '':
        users.id_name = data['id_name']

    if data['id_card'] != '':
        users.id_card = data['id_card']

    if data['address'] != '':
        users.address = data['address']

    if data['education']:
        users.education =data['education']

    if data['major']:
        users.major =data['major']

    if data['dgree']:
        users.dgree =data['dgree']

    if data['school']:
        users.school =data['school']

    # users.is_status = data['is_status']
    users.save()
    return JsonResponse({
        "status": "success",
        "message": "用户信息更改成功",
        "info": ""
    })
    # return HttpResponse(123)

#查看用户详情
def detailUser(request):
    user_id = request.POST.get('user_id',None)
    user = Users.objects.get(id=user_id)
    return render(request,'user/detailuser1.html',context={'user':user})

#修改密码
class EditPwd(View):
    def get(self,request):
        # 接受数据
        user_id =request.GET.get('user_id',None)
        users = Users.objects.get(id=user_id)
        # print(users.nickname)
        # print(users.password)
        if user_id:
            return render(request,'user/edit_pwd1.html',context={'users':users})

    def post(self,request):
        user_id = request.POST.get('user_id', None)
        info = Users.objects.filter(id=user_id).exists()
        # print(info)
        password = request.POST.get('password', None)
        # print(password)
        newPwd = make_password(password=password)
        # print(newPwd)
        users = Users.objects.get(id=user_id)
        users.password = newPwd
        users.save()
        return JsonResponse({
            "status":"success",
            "message":"成功",
            "info":""
        })

#修改用户头像
class UserImageUpload(View):
    def get(self,request):
        # 接收数据
        user_id =request.GET.get('user_id',None)
        users = Users.objects.get(id=user_id)
        return render(request, 'user/image_upload1.html', context={'users': users})

    def post(self,request):
        #上传数据
        user_id = request.POST.get('user_id',None)
        users  = Users.objects.get(id=user_id)
        # print(users.user_img)
        user_img = request.FILES.get('avatar')  #此处的avatar，是图片上传html的$("#submit-btn")里avatar
        try:
            users.user_img = user_img
            users.save()
            data = {'state':1}
        except:
            data = {'state':0}
        return JsonResponse(data)

#发送密码重置邮件
class RestartPwd(View):
    def get(self,request):
        user_id = request.GET.get('user_id', None)
        users = Users.objects.get(id=user_id)
        context = {
            'users':users
        }
        return render(request,'user/restart.html',context=context)


    def post(self,request):
        user_id = request.POST.get('user_id', None)
        users = Users.objects.get(id=user_id)
        email = users.email
        email_send.send_register_email(email)
        return HttpResponse(110)

def changePwd(request, active_code):
    record = EmailVerifyRecord.objects.filter(code=active_code)
    if record:
        for i in record:
            email = i.email
            users = Users.objects.get(email=email)
            if users:
                return render(request, 'user/pwd_reset.html', {'users': users})

#删除用户
class DelUser(View):
    def get(self,request):
        #判断当前id是否存在
        user_id = request.GET.get('user_id',None)
        users = Users.objects.get(id = user_id)  #获取所有选中id的信息
        context = {
            'users':users,
        }
        is_status = 0
        users.is_status = is_status
        users.save()
        # print(users.is_status)
        return render(request,'user/user_index1.html',context=context)

#已删除用户列表展示
def deldUser(request):
    users = Users.objects.filter(is_status=0)
    context = {'users': users}
    return render(request, 'user/deld_user.html', context=context)

#还原已删除用户
class UserUser(View):
    def get(self,request):
        #判断当前id是否存在
        user_id = request.GET.get('user_id',None)
        users = Users.objects.get(id = user_id)  #获取所有选中id的信息
        context = {
            'users':users,
        }
        is_status = 1
        users.is_status = is_status
        users.save()
        # print(users.is_status)
        return render(request,'user/deld_user.html',context=context)

#永久删除用户，删除用户存在数据库的信息
class DelesUser(View):
    def get(self,request):
        #获取id
        user_id = request.GET.get('user_id',None)
        users = Users.objects.get(id = user_id)  #获取所有选中id的信息
        context = {
            'users':users,
        }
        Users.objects.get(id=user_id).delete()
        return render(request,'user/deld_user.html',context=context)

#管理员列表展示
def adminView(request):
    admins = Admins.objects.all()
    context = {'admins': admins}
    return render(request, 'user/admin_list.html', context=context)

#添加管理员
class AddAdminView(View):
    def get(self,request):
        return render(request,'user/addadmin.html')

    def post(self,request):
        admin_name = request.POST.get('admin_name',None)
        password = request.POST.get('password',None)
        #判断管理员是否存在
        info = Admins.objects.filter(admin_name=admin_name).exists()
        if info:    #如果为true，控制台返回值
            return JsonResponse({
                'status':'fail',
                'message':'当前用户已存在',
                'tagid':'admin_name'
            })
        #如果不存在就增加管理员数据
        Admins.objects.create(
            admin_name=admin_name,
            password=password,
            req_ip = Base.get_ip(request),
            req_time=Base.getNowTime(request)
        )
        return JsonResponse({
            'status': 'success',
            'message': '创建成功',
            'info': ''
        })

#删除管理员,需要检测管理员账户名，如果当前管理员删除自己的账户，不通过
class DelAdmin(View):
    def get(self,request):
        #获取当前id，并判断是否在线
        admin_id = request.GET.get('admin_id',None)
        admins = Admins.objects.get(id = admin_id)  #获取选中id的信息
        context = {
            'admins':admins,
        }
        value = request.session.get("admin_name",None) #获取登录的用户的session，来判断能不能删除
        if value == admins.admin_name:    #如果相同，控制台返回值
            return JsonResponse({
                'status':'fail',
                'message':'正在登录状态，不允许删除！',  #其实没用上这句，html写了框
                'tagid':'value'
            })
        # print(value)
        # print(admins.admin_name)
        if value != admins.admin_name:
            is_status = 0
            admins.is_status = is_status
            admins.save()
        return render(request,'user/admin_list.html',context=context)

#还原已删除管理员
class AdminAdmin(View):
    def get(self,request):
        #判断当前id是否存在
        admin_id = request.GET.get('admin_id', None)
        admins = Admins.objects.get(id=admin_id)  # 获取选中id的信息
        context = {
            'admins': admins,
        }
        is_status = 1
        admins.is_status = is_status
        admins.save()
        # print(users.is_status)
        return render(request,'user/admin_list.html',context=context)

#永久删除管理员，删除存在数据库的信息
class DelesAdmin(View):
    def get(self,request):
        #获取id
        admin_id = request.GET.get('admin_id', None)
        admins = Admins.objects.get(id=admin_id)  # 获取选中id的信息
        context = {
            'admins': admins,
        }
        Admins.objects.get(id=admin_id).delete()
        return render(request,'user/admin_list.html',context=context)

