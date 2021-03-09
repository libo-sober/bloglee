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
from django.contrib import admin
from django.urls import path, re_path

from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 首页
    path('', views.Index.as_view(), name='index'),
    # 关于
    path('about/', views.About.as_view(), name='about'),
    # 文章详情
    re_path(r'^articles/detail/(\d+)/', views.ArticleView.as_view(), name='detail'),
    # 文章分类
    re_path(r'^articles/category/(\d+)/', views.CategoryView.as_view(), name='category'),
    # 增加评论
    re_path(r'^add_comment/(\d+)/', views.CategoryView.as_view(), name='add_comment'),

]
