# Generated by Django 2.2.13 on 2021-03-14 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_userinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='is_admin',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]