from django.db import models
from school.models import Schools

# Create your models here.
# 专业信息表
class Majors(models.Model):
    major_name = models.CharField("专业名称", max_length=255, null=False)
    major_desciption = models.CharField("专业简述", max_length=255, null=True)
    level = models.IntegerField("层次", default=0)  # 0:高起专  1:高起本  2：专升本
    school = models.ForeignKey("school.Schools", verbose_name="所属院校", on_delete=models.DO_NOTHING,related_name='school', null=True)
    major_category = models.ForeignKey("MajorCates", verbose_name="所属分类", on_delete=models.DO_NOTHING,related_name='major_category', null=True)
    is_recommend = models.IntegerField("是否推荐", default=0)  # 0不推荐 1 推荐
    times = models.FloatField("学制", null=True)
    count = models.BigIntegerField("报读人数", null=True)
    is_fast = models.BooleanField("是否录取快", default=False)  # false 否  true 是
    is_special = models.BooleanField("是否特色专业", default=False)  # false 否  true 是
    detail = models.TextField("专业介绍", null=True)
    is_status = models.BooleanField("状态", default=True)  # true 可用  false 不可用

    class Meta:
        verbose_name = "专业信息"
        verbose_name_plural = verbose_name
        db_table = "zhouju_majors"

# 专业分类表
class MajorCates(models.Model):
    catename = models.CharField("专业分类名", max_length=255, null=False)
    pid = models.IntegerField("父分类", null=True)
    is_status = models.BooleanField("状态", default=True)  # true 可用  false 不可用

    class Meta:
        verbose_name = "专业分类"
        verbose_name_plural = verbose_name
        db_table = "zhouju_major_cates"
