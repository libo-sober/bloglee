# Generated by Django 3.1.7 on 2021-03-16 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20210316_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='cover_img',
            field=models.ImageField(default='covers/head.jpg', upload_to='covers/'),
        ),
        migrations.AlterField(
            model_name='file',
            name='cover_file',
            field=models.FileField(default='covers/head.jpg', upload_to='covers/'),
        ),
    ]
