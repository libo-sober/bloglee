# Generated by Django 2.2.13 on 2021-03-09 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='qq_email',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='qq邮箱'),
        ),
        migrations.AddField(
            model_name='comment',
            name='web_site',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='网站'),
        ),
    ]
