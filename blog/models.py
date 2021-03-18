from django.db import models
from django.utils.html import format_html
from mdeditor.fields import MDTextField
from datetime import datetime
# Create your models here.



class UserInfo(models.Model):
    """用户信息表"""
    username = models.CharField(max_length=16, verbose_name='姓名')
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    avatar = models.FileField(upload_to='avatars/', default=None)

    class Meta:
        verbose_name_plural = '用户信息表'

    def __str__(self):  # __unicode__

        return self.username




class Column(models.Model):
    """
    文章专栏
    """
    name = models.CharField(max_length=30, verbose_name='专栏名称')
    url = models.CharField(max_length=10, null=True, blank=True, default='None', verbose_name='路径')
    icon = models.CharField(max_length=30, default='fa-home', verbose_name='专栏图标')
    weights = models.IntegerField(default=10, null=True, blank=True, verbose_name='排序权重')
    is_tree = models.BooleanField(default=False, null=True, blank=True, verbose_name='添加儿子')

    class Meta:
        verbose_name = '专栏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(max_length=30, verbose_name='标签名称')

    # 统计文章数 并放入后台
    def get_items(self):
        return len(self.article_set.all())

    get_items.short_description = '文章数'

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=99, verbose_name='分类排序')
    active = models.BooleanField(default=True, verbose_name='是否添加到菜单')
    icon = models.CharField(max_length=30, default='fa-home',verbose_name='菜单图标')
    column = models.ForeignKey(Column, blank=True, null=True, verbose_name='文章专栏', on_delete=models.CASCADE)

    # 统计文章数 并放入后台
    def get_items(self):
        return len(self.article_set.all())

    def icon_data(self):
        return format_html(
            '<i class="{}"></i>',
            self.icon,
        )

    get_items.short_description = '文章数'
    icon_data.short_description = '图标预览'

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    文章
    """
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.TextField(max_length=100, verbose_name='文章描述')
    # cover = models.CharField(max_length=200, default='https://image.3001.net/images/20200304/15832956271308.jpg', verbose_name='文章封面')
    cover = models.FileField(upload_to='covers/', default='covers/1P629140610-3.jpg', verbose_name='文章封面')
    content = MDTextField(verbose_name='文章内容')  # 富文本编辑框，要在models中注册mdeditor
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    upup = models.IntegerField(default=0, verbose_name='点赞次数', null=True, blank=True)
    comments = models.IntegerField(default=0, verbose_name='评论次数', null=True, blank=True)
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')  # 置顶
    # TODO libo: 几条评论
    add_time = models.DateTimeField(default=datetime.now, verbose_name='发布时间')

    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='文章分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')

    def cover_data(self):
        return format_html(
            '<img src="{}" width="156px" height="98px"/>',
            self.cover,
        )

    def cover_admin(self):
        return format_html(
            '<img src="{}" width="440px" height="275px"/>',
            self.cover,
        )

    def upuped(self):
        """
        增加点赞数
        :return:
        """
        self.upup += 1
        self.save(update_fields=['upup'])

    def commented(self):
        """
        增加评论数
        :return:
        """
        self.comments += 1
        self.save(update_fields=['comments'])

    def viewed(self):
        """
        增加阅读数
        """
        self.click_count += 1
        self.save(update_fields=['click_count'])

    cover_data.short_description = '文章封面'
    cover_admin.short_description = '文章封面'

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    文章评论
    """
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, verbose_name='用户名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)
    qq_email = models.CharField(max_length=100, verbose_name='qq邮箱')  # 应该关联到userinfo表中的email子段
    web_site = models.CharField(max_length=100, blank=True, null=True, verbose_name='网站')
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:20]


class Links(models.Model):
    """
    友情链接
    """
    title = models.CharField(max_length=50, verbose_name='标题')
    url = models.URLField(verbose_name='地址')
    desc = models.TextField(verbose_name='描述', max_length=250, null=True, blank=True)
    image = models.URLField(default='/media/avatas/head.jpg', verbose_name='头像')
    is_disply = models.BooleanField(default=False, null=True, blank=True)

    def avatar_data(self):
        return format_html(
            '<img src="{}" width="50px" height="50px" style="border-radius: 50%;" />',
            self.image,
        )

    def avatar_admin(self):
        return format_html(
            '<img src="{}" width="250px" height="250px"/>',
            self.image,
        )

    avatar_data.short_description = '头像'
    avatar_admin.short_description = '头像预览'

    class Meta:
        verbose_name = '友链'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.url


class Site(models.Model):
    """
    站点配置
    """
    desc = models.CharField(max_length=50, verbose_name='网站描述')
    keywords = models.CharField(max_length=50, verbose_name='网站关键词')
    title = models.CharField(max_length=50, verbose_name='网站标题')
    index_title = models.CharField(max_length=50, verbose_name='首页标题')
    type_chinese = models.CharField(max_length=50, verbose_name='座右铭汉语')
    type_english = models.CharField(max_length=80, verbose_name='座右铭英语')
    icp_number = models.CharField(max_length=20, verbose_name='备案号')
    icp_url = models.CharField(max_length=50, verbose_name='备案链接')
    site_mail = models.CharField(max_length=50, verbose_name='我的邮箱')
    site_qq = models.CharField(max_length=50, verbose_name='我的QQ')
    site_avatar = models.CharField(max_length=200, default='/avatars/head.jpg', verbose_name='我的头像')

    class Meta:
        verbose_name = '网站设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class File(models.Model):

    file = models.FileField(upload_to='covers/', default='covers/head.jpg')
    class Meta:
        verbose_name = '文件上传'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.file.name



class About(models.Model):
    me = MDTextField( verbose_name='关于博主')
    site = MDTextField( verbose_name='关于本站')
    promise = MDTextField( verbose_name='本站声明')
    class Meta:
        verbose_name = '关于我'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.me[:10]
