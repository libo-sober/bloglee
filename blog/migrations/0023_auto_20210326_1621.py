# Generated by Django 3.1.7 on 2021-03-26 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20210318_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='最后登录时间'),
        ),
        migrations.AlterField(
            model_name='site',
            name='site_avatar',
            field=models.CharField(default='/avatars/head.jpg', max_length=200, verbose_name='我的头像'),
        ),
    ]
