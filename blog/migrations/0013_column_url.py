# Generated by Django 3.1.7 on 2021-03-16 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210316_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='url',
            field=models.CharField(blank=True, default='None', max_length=10, null=True, verbose_name='路径'),
        ),
    ]
