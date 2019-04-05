from django.db import models
from user.models import Areas, Provinces, Citys

# Create your models here.

# 院校类型表
class SchoolType(models.Model):
    type_name = models.CharField("类型名称", max_length=255)
    notes = models.TextField("分类说明", null=True)
    is_status = models.BooleanField("状态", default=True)  # true 可用 false 不可用

    class Meta:
        verbose_name = "院校类型表"
        verbose_name_plural = "院校类型"
        db_table = "zhouju_school_type"

# 院校特征表
class SchoolFeatures(models.Model):
    feature_name = models.CharField("院校特征名称", max_length=255)
    notes = models.TextField("院校特征说明", null=True)
    is_status = models.BooleanField("状态", default=True)  # true 可用  false 不可用

    class Meta:
        verbose_name = "院校特征表"
        verbose_name_plural = "院校特征"
        db_table = "zhouju_school_features"

# 院校表
class Schools(models.Model):
    name = models.CharField("院校名称", max_length=255)
    banner = models.FileField("院校banner图", upload_to='media', null=True)  # 图片地址
    description = models.TextField("院校描述")
    motto = models.TextField("校训", null=True)
    emblem = models.FileField("校徽", upload_to='media', null=True)  # 校徽图片地址
    enrol_notes = models.TextField("报名须知", null=True)
    diploma_images = models.FileField("毕业证图片地址", upload_to='media', null=True)
    degree_images = models.FileField("学位证图片地址", upload_to='media', null=True)
    is_985 = models.BooleanField("是否是985", default=False)  # True 是985 False 不是985
    is_211 = models.BooleanField("是否是211", default=False)  # True 是211，False 不是211
    is_double = models.BooleanField("是否是双一流", default=False)  # True 是双一流， False 不是
    brief = models.TextField("招生简章", null=True)
    exam = models.TextField("考试与毕业", null=True)
    count = models.BigIntegerField("累计报读人数", null=True)
    is_status = models.BooleanField("状态", default=True)  # true 可用  false 不可用

    sch_pro = models.ForeignKey("user.Provinces", verbose_name="院校所在省份", on_delete=models.DO_NOTHING,
                                related_name='sch_pro', null=True)
    sch_city = models.ForeignKey("user.Citys", verbose_name="院校所在城市", on_delete=models.DO_NOTHING,
                                 related_name='sch_city', null=True)
    school_type = models.ManyToManyField("SchoolType", verbose_name="学校类型")
    scholl_feature = models.ManyToManyField("SchoolFeatures", verbose_name="学校特性")


    class Meta:
        verbose_name = "院校表"
        verbose_name_plural = "院校列表"
        db_table = "zhouju_schools"