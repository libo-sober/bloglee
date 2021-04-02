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
from django.conf.urls import url
from django.views.static import serve
from blog.feeds import BlogRssFeed

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # 首页
    path('', views.Index.as_view(), name='index'),
    # 登录
    path('login/', views.LoginView.as_view(), name='login'),
    # 登出
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # 个人资料
    path('userinfo/detail/', views.UserInfoView.as_view(), name='userinfo'),
    path('modify/password/', views.ModifyView.as_view(), name='modify'),
    # 注册
    path('register/', views.RegisterView.as_view(), name='register'),
    # 关于
    path('about/', views.About.as_view(), name='about'),
    # 文章详情
    re_path(r'^articles/detail/(?P<en_us>.*)/', views.ArticleView.as_view(), name='detail'),
    # 文章分类
    re_path(r'^articles/category/(?P<en_us_c>.*)/', views.Index.as_view(), name='category'),
    # 文章按标签分
    re_path(r'^articles/tag/(?P<en_us_c>.*)/(?P<en_us_tag>.*)/', views.Index.as_view(), name='tag'),
    # 评论
    path('comment/', views.CommentView.as_view(), name='comment'),
    # 点赞
    path('article/love/', views.LoveView.as_view(), name='love'),
    # 归档
    path('archive/', views.ArchiveView.as_view(), name='archive'),
    # 友情链接
    path('friends/', views.FriendsView.as_view(), name='friends'),
    # 留言
    path('messages/', views.MessagesView.as_view(), name='messages'),
    # 搜索
    path('article/search/', views.SearchView.as_view(), name='search'),
    # mdeditor
    path('mdeditor/', include('mdeditor.urls')),
    # RSS订阅
    path('rss/', BlogRssFeed(), name='rss'),
    # 激活用户
    re_path(r'activation/(?P<active_code>.*)/', views.Activate.as_view(), name='activation'),
    # url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),

    # url(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),

]
# 设置后台名称
admin.site.site_header = '大聪明博客后台'
admin.site.site_title = 'Django Blog 后台'

# 404
handler404 = "blog.views.page_not_found"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



