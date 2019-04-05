from django.db import models
from school.models import Schools
from major.models import Majors

# Create your models here.

# 服务中心分类表
class ServerCategorys(models.Model):
    server_name = models.CharField("分类名称", max_length=255)
    is_status = models.BooleanField("状态", default=True)  # true 可用 false 不可用

    class Meta:
        verbose_name = "服务中心分类表"
        verbose_name_plural = "服务中心分类"
        db_table = "zhouju_server_categorys"

#附件表
class Attachments(models.Model):
    atta_name = models.CharField("附件名称", max_length=255)
    addtime= models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    filename= models.URLField("存储链接", max_length=255, null=True)
    is_status = models.BooleanField("状态", default=True)  # true 可用 false 不可用

    class Meta:
        verbose_name = "服务中心附件表"
        verbose_name_plural = "附件表"
        db_table = "zhouju_attachments"

#关键词表
class Keywords(models.Model):
    key_name = models.CharField(verbose_name='关键字', max_length=64)

    class Meta:
        verbose_name = "关键字表"
        verbose_name_plural = "关键字"
        db_table = "zhouju_keywords"

#教学中心表
class Centers(models.Model):
    cen_name= models.CharField("中心名称", max_length=255)
    cen_num = models.IntegerField("编号", null=True)
    address= models.CharField("地址", max_length=255, null=True)
    phone = models.CharField('电话', max_length=255, null=True)
    is_direct= models.IntegerField("是否直属", default=1) # 0否 1 是
    is_status = models.BooleanField("状态", default=True)  # true 可用 false 不可用

    class Meta:
        verbose_name = "教学中心表"
        verbose_name_plural = "教学中心表"
        db_table = "zhouju_centers"

#服务中心文章表
class ServerPosts(models.Model):
    post_title = models.CharField("文章标题", max_length=255, null=False)
    source = models.CharField("文章来源", max_length=255, null=True, default="舟炬教育")
    source_link = models.URLField("来源链接", max_length=255, null=True, default="http://www.zhoujuedu.com")
    post_content = models.TextField("文章内容", null=True)
    edit_time = models.DateTimeField("编辑时间", auto_now=True)
    views = models.IntegerField("阅读人数", default=0)

    cateid = models.ForeignKey("ServerCategorys", verbose_name='服务中心分类', on_delete=models.DO_NOTHING, related_name='cateid', null=True)
    keywords = models.ForeignKey("Keywords", verbose_name='关键字', on_delete=models.DO_NOTHING, related_name='keywords', null=True)
    server_post_school = models.ForeignKey("school.Schools", verbose_name="所属院校", on_delete=models.DO_NOTHING,related_name='server_post_school', null=True)
    is_status = models.BooleanField("状态", default=True)  # true 可用  false 不可用

    class Meta:
        verbose_name = "服务中心文章"
        verbose_name_plural = verbose_name
        db_table = 'zhouju_server_posts'

#模拟题表
class Aquestions(models.Model):
    ques_name = models.CharField("附件名称", max_length=255)
    ques_filename = models.URLField("存储链接", max_length=255, null=True)
    adddtime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    is_status = models.BooleanField("状态", default=True)  # true 可用  false 不可用

    ques_school = models.ForeignKey("school.Schools", verbose_name="院校名称", on_delete=models.DO_NOTHING,related_name='ques_school', null=True)
    ques_major = models.ForeignKey("major.Majors", verbose_name="专业名称", on_delete=models.DO_NOTHING,related_name='ques_major',null=True)
    ques_level = models.ForeignKey("major.Majors", verbose_name="专业层次", on_delete=models.DO_NOTHING,related_name='ques_level', null=True)

    class Meta:
        verbose_name = "模拟题表"
        verbose_name_plural = verbose_name
        db_table = 'zhouju_aquestions'