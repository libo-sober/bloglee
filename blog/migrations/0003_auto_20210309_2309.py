# Generated by Django 2.2.13 on 2021-03-09 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210309_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='qq_email',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='qq邮箱'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='web_site',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='网站'),
        ),
    ]
