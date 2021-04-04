import mistune

from bs4 import BeautifulSoup
from django.contrib import admin
from blog import models
from django import forms
# Register your models here.


admin.site.site_header = "后台管理系统"
admin.site.site_title = "欢迎进入后台管理~"
admin.site.index_title = "大聪明博客"

# admin.site.register(models.Article)
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Links)
admin.site.register(models.Site)
admin.site.register(models.UserInfo)
admin.site.register(models.Column)
admin.site.register(models.File)
admin.site.register(models.About)
admin.site.register(models.EmailVerifyRecord)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = "__all__"

    def clean_desc(self):

        desc = self.cleaned_data['desc']
        content = self.data['content']
        renderer = mistune.Renderer(escape=True, hard_wrap=True)
        # renderer = HighlightRenderer()
        mk = mistune.Markdown(renderer=renderer)
        output = mk(content)
        soup = BeautifulSoup(output, 'html.parser')
        content = soup.text[:150]
        print(desc)
        if desc:
            return desc
        else:
            desc = content
            return desc


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm







