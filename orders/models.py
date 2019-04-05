from django.db import models
from school.models import Schools
from major.models import MajorCates,Majors
from user.models import Users

# Create your models here.

# 报名订单信息
class Orders(models.Model):
    STATUS_LIST = (
        ('wfk', "未付款"),
        ('yfk', "已付款"),
        ('ylq', "已录取"),
        ('ysx', "已失效")
    )

    real_name = models.CharField("真实姓名", max_length=255, null=False)  # 添加时要更新用户列表信息，这三个
    idcard = models.CharField("身份证号", max_length=18, null=False)
    phone = models.CharField("电话", max_length=255, null=False)

    user = models.ForeignKey("user.Users", verbose_name="用户id", on_delete=models.DO_NOTHING, related_name='user', null=False)
    major_cates = models.ForeignKey("major.MajorCates", verbose_name="专业分类", on_delete=models.DO_NOTHING,related_name='major_cates', null=False)
    major = models.ForeignKey("major.Majors", verbose_name="专业名称", on_delete=models.DO_NOTHING, related_name='major',null=False)
    order_level = models.ForeignKey("major.Majors", verbose_name="专业层次", on_delete=models.DO_NOTHING, related_name='order_level', null=False)
    order_school = models.ForeignKey("school.Schools", verbose_name="院校名称", on_delete=models.DO_NOTHING, related_name='order_school', null=False)

    status = models.CharField("付款录取状态", max_length=11, choices=STATUS_LIST, default='wfk')
    is_status = models.BooleanField("状态", default=True)  # true 可用  false 不可用
    # 一个专业有几个层次就写几个专业，一个个层次写，专业表，专业类型表和院校表多添加几个吧
    #先选专业，在选层次，在选院校

    class Meta:
        verbose_name = "报名订单信息"
        verbose_name_plural = verbose_name
        db_table = "zhouju_orders"

