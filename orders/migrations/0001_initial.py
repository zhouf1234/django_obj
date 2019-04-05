# Generated by Django 2.1.3 on 2019-01-25 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0006_emailverifyrecord'),
        ('major', '0001_initial'),
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_name', models.CharField(max_length=255, verbose_name='真实姓名')),
                ('idcard', models.CharField(max_length=18, verbose_name='身份证号')),
                ('phone', models.CharField(max_length=255, verbose_name='电话')),
                ('status', models.CharField(choices=[('wfk', '未付款'), ('yfk', '已付款'), ('ylq', '已录取'), ('ysx', '已失效')], default='wfk', max_length=11, verbose_name='付款录取状态')),
                ('is_status', models.BooleanField(default=True, verbose_name='状态')),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='major', to='major.Majors', verbose_name='专业名称')),
                ('major_cates', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='major_cates', to='major.MajorCates', verbose_name='专业分类')),
                ('order_level', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_level', to='major.Majors', verbose_name='专业层次')),
                ('order_school', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_school', to='school.Schools', verbose_name='院校名称')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to='user.Users', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '报名订单信息',
                'verbose_name_plural': '报名订单信息',
                'db_table': 'zhouju_orders',
            },
        ),
    ]