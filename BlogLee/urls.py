"""BlogLee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from BlogLee import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 首页
    path('', views.Index.as_view(), name='index'),
    # 登录
    path('login/', views.LoginView.as_view(), name='login'),
    # 注册
    path('register/', views.RegisterView.as_view(), name='register'),
    # 关于
    path('about/', views.About.as_view(), name='about'),
    # 文章详情
    re_path(r'^articles/detail/(\d+)/', views.ArticleView.as_view(), name='detail'),
    # 文章分类
    re_path(r'^articles/category/(\d+)/', views.Index.as_view(), name='category'),
    # 文章按标签分
    re_path(r'^articles/tag/(\d+)/(\d+)/', views.Index.as_view(), name='tag'),
    # 评论
    path('comment/', views.CommentView.as_view(), name='comment'),
    # mdeditor
    path('mdeditor/', include('mdeditor.urls')),


]
# 设置后台名称
admin.site.site_header = '大聪明博客后台'
admin.site.site_title = 'Django Blog 后台'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
