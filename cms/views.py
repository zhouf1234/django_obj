'''
项目备注信息:
1. 当前视图里面的所有类都可以有选择的继承Base基类
2. 前台和后台采用ajax异步来进行消息传递，消息传递采用json得到形式，结构如下:
    {
        "status":"success/fail"
        "message":"具体消息"
        "info":"备注或者消息补充"
    }

    前台->给我100块
    后台->给  {
        "status":"success"
        "message":"大哥，钱我给你，人能不能放了"
        "info":"大哥，真没钱了，最后一百了"
    }
3. 使用哪个key来在session中代表登录名，不能轻易更改
'''

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from cms.check import Base
from .models import Admins

class IndexView(Base):      #先写了check.py的基类base
    def get(self, request):
        # 判断用户是否登录
        status = Base.checkUserLogin(request)
        if status:
            # 获取ip和时间
            ip = Base.get_ip(request)
            info_time = Base.getNowTime(request)
            # 将数据传递给前台
            context = {
                'ip': ip,
                'info_time': info_time
            }
            return render(request, 'cms/index1.html', context=context)
        else:
            return render(request, 'cms/login1.html')

    def post(self, request):
        pass


class LoginView(Base):
    def get(self, request):
        # 检查登录状态
        login_status = Base.checkUserLogin(request)
        if login_status:
            return render(request, 'cms/index1.html')
        else:
            return render(request, 'cms/login1.html')

    def post(self, request):
        # 接收一下后台传递过来的值
        check_name = request.POST.get("admin_name", None)
        check_password = request.POST.get("password", None)
        # 对数据进行验证，用户名和密码是否规范合理
        check_status = Base.check_data(check_name, check_password)
        # 判断当前用户是否存在
        info = Admins.objects.filter(admin_name=check_name).exists()
        if info and check_status['errors'] is None:
            #判断账户是否可用
            status = Admins.objects.get(admin_name=check_name).is_status
            if status == 0:
                return JsonResponse({
                    "status": "fail",
                    "message": "登录失败。账户不可用!",
                    "info": "请更改密码"
                })
            # 判断密码是否和数据库一致
            pwd = Admins.objects.get(admin_name=check_name).password
            if pwd == check_password:
                ip = Base.get_ip(request)
                info = Admins.objects.get(admin_name=check_name)
                info.last_ip = ip
                info.save()
                request.session['admin_name'] = check_name
                # url_info = "/cms/index/" # 访问成功后跳转的路径
                url_info = "/cms/"      #因为检查登录状态那里已经写了跳转路径，所以此处只用写cms就可，否则会跳错
                return JsonResponse({
                    "status":"success",
                    "message":"登录成功，可以进入后台首页",
                    "info": url_info
                })
            else:
                return JsonResponse({
                    "status": "fail",
                    "message": "登录失败。密码错误",
                    "info": "请更改密码"
                })
        elif info is False:
            return JsonResponse({
                "status": "fail",
                "message": "当前用户不存在",
                "info": "请检查用户名"
            })
        elif check_status['errors'] is not None:
            return JsonResponse({
                "status": "fail",
                "message": "登录信息有误",
                "info": check_status['errors']
            })
        else:
            return JsonResponse({
                "status": "fail",
                "message": "当前登录信息发生了不可知的错误，请重新输入",
                "info": ""
            })




