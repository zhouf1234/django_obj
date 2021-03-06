# Generated by Django 2.1.3 on 2019-02-20 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('major', '0001_initial'),
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aquestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ques_name', models.CharField(max_length=255, verbose_name='附件名称')),
                ('ques_filename', models.URLField(max_length=255, null=True, verbose_name='存储链接')),
                ('adddtime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('is_status', models.BooleanField(default=True, verbose_name='状态')),
                ('ques_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ques_level', to='major.Majors', verbose_name='专业层次')),
                ('ques_major', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ques_major', to='major.Majors', verbose_name='专业名称')),
                ('ques_school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ques_school', to='school.Schools', verbose_name='院校名称')),
            ],
            options={
                'verbose_name': '模拟题表',
                'verbose_name_plural': '模拟题表',
                'db_table': 'zhouju_aquestions',
            },
        ),
        migrations.CreateModel(
            name='Attachments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atta_name', models.CharField(max_length=255, verbose_name='附件名称')),
                ('addtime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('filename', models.URLField(max_length=255, null=True, verbose_name='存储链接')),
                ('is_status', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '服务中心附件表',
                'verbose_name_plural': '附件表',
                'db_table': 'zhouju_attachments',
            },
        ),
        migrations.CreateModel(
            name='Centers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cen_name', models.CharField(max_length=255, verbose_name='中心名称')),
                ('cen_num', models.IntegerField(null=True, verbose_name='编号')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='地址')),
                ('phone', models.CharField(max_length=255, null=True, verbose_name='电话')),
                ('is_direct', models.IntegerField(default=1, verbose_name='是否直属')),
                ('is_status', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '教学中心表',
                'verbose_name_plural': '教学中心表',
                'db_table': 'zhouju_centers',
            },
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_name', models.CharField(max_length=64, verbose_name='关键字')),
            ],
            options={
                'verbose_name': '关键字表',
                'verbose_name_plural': '关键字',
                'db_table': 'zhouju_keywords',
            },
        ),
        migrations.CreateModel(
            name='ServerCategorys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_name', models.CharField(max_length=255, verbose_name='分类名称')),
                ('is_status', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '服务中心分类表',
                'verbose_name_plural': '服务中心分类',
                'db_table': 'zhouju_server_categorys',
            },
        ),
        migrations.CreateModel(
            name='ServerPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=255, verbose_name='文章标题')),
                ('source', models.CharField(default='舟炬教育', max_length=255, null=True, verbose_name='文章来源')),
                ('source_link', models.URLField(default='http://www.zhoujuedu.com', max_length=255, null=True, verbose_name='来源链接')),
                ('post_content', models.TextField(null=True, verbose_name='文章内容')),
                ('edit_time', models.DateTimeField(auto_now=True, verbose_name='编辑时间')),
                ('views', models.IntegerField(default=0, verbose_name='阅读人数')),
                ('is_status', models.BooleanField(default=True, verbose_name='状态')),
                ('cateid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cateid', to='server.ServerCategorys', verbose_name='服务中心分类')),
                ('keywords', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='keywords', to='server.Keywords', verbose_name='关键字')),
                ('server_post_school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='server_post_school', to='school.Schools', verbose_name='所属院校')),
            ],
            options={
                'verbose_name': '服务中心文章',
                'verbose_name_plural': '服务中心文章',
                'db_table': 'zhouju_server_posts',
            },
        ),
    ]
