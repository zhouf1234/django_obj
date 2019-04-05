from django.views import View
import re
from django.utils import timezone



# 创建一个基类
class Base(View):
    # 获取当前时间
    def getNowTime(request):
        info_time = timezone.now()
        return info_time

    # 验证用户是否登录
    def checkUserLogin(request):
        if request.session.get("admin_name",None) is not None:
            return True
        else:
            return False


    # 获取用户IP
    def get_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        return ip

    # 对数据进行合法化验证
    def check_data(name,password):
        # 创建一个字典
        res = {
            'name':None,
            'pwd':None,
            'errors':None
        }
        # 用户名规则:最短6位，最长15位，以字母开头，后续可以是数字字母下滑线
        name_re  = re.compile(r'^[a-zA-Z].{5,14}$')
        # 密码规则:最短6位，最长18位，以字母开头
        password_re = re.compile(r'^[a-zA-Z].{5,17}$')
        if len(name) >=6 and len(password)>=6:
            res['name'] = name_re.match(name)
            res['pwd'] = password_re.match(password)

            if res['name'] == None or res['pwd'] == None:
                res['errors'] = '用户名或者密码不符合规则'

            return res
        else:
            res['errors'] = "用户名和密码长度不能小于6位"
            return res