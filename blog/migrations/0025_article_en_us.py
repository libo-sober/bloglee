# Generated by Django 3.1.7 on 2021-04-01 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20210331_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='en_us',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='英文标题'),
        ),
    ]
