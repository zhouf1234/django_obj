# Generated by Django 2.1.3 on 2019-01-25 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='school',
        ),
        migrations.AddField(
            model_name='posts',
            name='post_school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_school', to='school.Schools', verbose_name='所属院校'),
        ),
    ]
