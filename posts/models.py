from django.db import models
from school.models import Schools

# Create your models here.
# 文章
class Posts(models.Model):
    post_title = models.CharField("文章标题", max_length=255, null=False)
    post_image = models.FileField("文章封面图片", upload_to='media' ,null=True)
    source = models.CharField("文章来源", max_length=255, null=True, default="舟炬教育")
    source_link = models.URLField("来源链接", max_length=255, null=True, default="http://www.zhoujuedu.com")
    post_content = models.TextField("文章内容",null=True)
    edit_time = models.DateTimeField("编辑时间", auto_now=True)
    views = models.IntegerField("阅读人数", default=0)
    tags = models.ForeignKey("Tag", verbose_name='标签', on_delete=models.DO_NOTHING,related_name='tags', null=True)
    is_status = models.BooleanField("状态", default=True)  # true 可用  false 不可用
    post_school = models.ForeignKey("school.Schools", verbose_name="所属院校", on_delete=models.DO_NOTHING,related_name='post_school', null=True)	#学员风采并未说明院校，暂时不填


    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        db_table = 'zhouju_posts'


# 标签表
class Tag(models.Model):
    name = models.CharField(verbose_name='标签名', max_length=64)	#就四个，学员风采，院校新闻，院校相关问题，院校通知公告，先就这四个吧
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    # 使对象在后台显示更友好，实例化
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '标签名称'  # 指定后台显示模型名称
        verbose_name_plural = '标签列表'  # 指定后台显示模型复数名称
        db_table = "zhouju_tag"  # 数据库表名
