from django.contrib import admin
from blog import models
# Register your models here.


admin.site.site_header = "后台管理系统"
admin.site.site_title = "欢迎进入后台管理~"
admin.site.index_title = "大聪明博客"

admin.site.register(models.Article)
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Links)
admin.site.register(models.Site)


