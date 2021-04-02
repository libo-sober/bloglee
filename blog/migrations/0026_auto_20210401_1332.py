# Generated by Django 3.1.7 on 2021-04-01 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_article_en_us'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='en_us',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='英文标题'),
        ),
        migrations.AddField(
            model_name='tag',
            name='en_us',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='英文标题'),
        ),
    ]