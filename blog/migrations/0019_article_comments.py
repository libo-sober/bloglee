# Generated by Django 3.1.7 on 2021-03-17 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_article_upup'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='comments',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='评论次数'),
        ),
    ]
