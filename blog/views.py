import datetime
import mistune
import re

from django.core.exceptions import ValidationError
from django import forms
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.base import View
from blog import models
from blog.utils.page_html import MyPagination
from django.core.mail import send_mail
from BlogLee import settings
from blog.utils.hashlib_func import set_md5
from django.contrib.auth.models import User

# Create your views here.
time = datetime.datetime(year=2099, month=1, day=1)


class Index(View):

    def get(self, request, cid=None, tag_id=None):
        """首页展示"""
        # 文章总数
        article_count = models.Article.objects.count()
        # 评论总数
        comment_count = models.Comment.objects.count()
        page_id = request.GET.get('page')  # 获取get请求中的page数据
        num = models.Article.objects.all().count()  # 总共记录数
        base_url = request.path  # 请求路径
        get_data = request.GET.copy()  # 直接调用这个类自己的copy方法或者deepcopy方法或者自己import copy 都可以实现内容允许修改
        # models.Article.objects.filter(is_recommend=1).update(add_time=time)  # <QuerySet [<Article: 太黑的诱惑>]>
        # all_articles = models.Article.objects.all().order_by('-add_time')  # <QuerySet [<Article: 333>]>
        top_articles = list(models.Article.objects.filter(is_recommend=1).order_by('-add_time'))
        articles = list(models.Article.objects.filter(is_recommend=False).order_by('-add_time'))
        all_articles = top_articles + articles
        # 以后直接在settings配置文件中修改即可
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录
        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count, record=record)
        # all_articles = articles | top_articles  # 合并两个queryset
        all_articles = all_articles[
                       (html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]

        # 文章分类
        categories = models.Category.objects.all()

        # 最新文章
        new_articles = models.Article.objects.all().order_by('-add_time')[:5]
        # 最热文章
        hot_articles = models.Article.objects.all().order_by('-click_count')[:5]
        # 最新评论
        new_comments = models.Comment.objects.all().order_by('-add_time')[:5]
        # 标签云
        tags = models.Tag.objects.all()
        # 登录的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
            qq_number = cur_user_name.email[:-7]
        else:
            cur_user_name = None
            qq_number = None

        qq_url = f'http://q.qlogo.cn/headimg_dl?dst_uin={qq_number}&spec=640&img_type=jpg'

        # 管理员用户对象
        admin_obj = models.UserInfo.objects.filter(is_admin=True).first()
        admin_url = 'http://127.0.0.1:8000/static/image/snd51t4nl2osnd51t4nl2o.png'   # 后期改为域名,不指定的话就用qq头像


        if tag_id:
            # tag_id对应类下的所有文章
            tags_num = models.Article.objects.filter(tag__pk=tag_id).count()  # 总共记录数
            tags_top_articles = list(
                models.Article.objects.filter(tag__pk=tag_id).filter(is_recommend=1).order_by('-add_time'))
            tags_articles = list(
                models.Article.objects.filter(tag__pk=tag_id).filter(is_recommend=False).order_by('-add_time'))
            tags_all_articles = tags_top_articles + tags_articles
            html_obj = MyPagination(page_id=page_id, num=tags_num, base_url=base_url, get_data=get_data,
                                    page_count=page_count, record=record)
            tags_all_articles = tags_all_articles[
                           (html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
            return render(request, 'tag.html',
                          {'tags_all_articles': tags_all_articles, 'page_html': html_obj.html_page(),
                           'categories':
                               categories, 'article_count': article_count, 'comment_count': comment_count,
                           'new_articles': new_articles, 'hot_articles':
                               hot_articles, 'new_comments': new_comments, 'tags': tags, 'cur_user_name': cur_user_name,
                           'qq_url': qq_url, 'admin_obj': admin_obj, 'admin_url': admin_url, })

        elif cid:
            # categoriy_id对应类下的所有文章
            categories_num = models.Article.objects.filter(category_id=cid).all().count()  # 总共记录数
            categories_top_articles = list(
                models.Article.objects.filter(category_id=cid).filter(is_recommend=1).order_by('-add_time'))
            categories_articles = list(
                models.Article.objects.filter(category_id=cid).filter(is_recommend=False).order_by('-add_time'))
            categories_all_articles = categories_top_articles + categories_articles
            html_obj = MyPagination(page_id=page_id, num=categories_num, base_url=base_url, get_data=get_data,
                                    page_count=page_count, record=record)
            categories_all_articles = categories_all_articles[
                                (html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
            return render(request, 'category.html', {'categories_all_articles': categories_all_articles,'page_html': html_obj.html_page(), 'categories':
                categories, 'article_count': article_count, 'comment_count': comment_count, 'new_articles': new_articles, 'hot_articles':
                hot_articles, 'new_comments': new_comments, 'tags': tags, 'cur_user_name': cur_user_name, 'qq_url': qq_url, 'admin_obj': admin_obj, 'admin_url': admin_url, })
        else:
            return render(request, 'index.html',
                          {'all_articles': all_articles, 'page_html': html_obj.html_page(), 'categories':
                              categories, 'article_count': article_count, 'comment_count': comment_count,
                           'new_articles': new_articles, 'hot_articles':
                               hot_articles, 'new_comments': new_comments, 'tags': tags, 'cur_user_name': cur_user_name, 'qq_url': qq_url, 'admin_obj': admin_obj, 'admin_url': admin_url, })


# 文章详情页
class ArticleView(View):

    def get(self, request, article_id=None):
        article = models.Article.objects.get(pk=article_id)
        article.viewed()  # 增加阅读数P
        # 为甚么刷新页面会产生两次访问ArticleView
        # 已经解决，因为文章中的请求js或者csss图片等路径为空或出错的，就会自动请求当前路径
        mk = mistune.Markdown()
        output = mk(article.content)

        # 文章分类
        categories = models.Category.objects.all()
        # 该文章的所有评论
        comment_obj = models.Comment.objects.filter(article_id=article_id).order_by('-add_time')
        comment_list = self.build_msg(comment_obj)
        ret = self.get_comment_list(comment_list)

        # 登录的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None

        return render(request, 'datail.html', {'article': article, 'detail_html': output, 'categories': categories, 'ret':
            ret, 'cur_user_name': cur_user_name, })

    def get_comment_list(self, comment_list):
        # 把msg增加一个chirld键值对，存放它的儿子们
        ret = []
        comment_dic = {}
        for comment_obj in comment_list:
            comment_obj['children'] = []
            comment_dic[comment_obj['pk']] = comment_obj

        for comment in comment_list:
            p_obj = comment_dic.get(comment['pid'])
            if not p_obj:
                ret.append(comment)
            else:
                p_obj['children'].append(comment)
        return ret

    def build_msg(self, comment_obj):
        # 把数据造成列表里边套字典的形式
        msg = []
        for comment in comment_obj:
            data = {}
            if comment.pid:
                data['pid'] = comment.pid.id
                data['fu_username'] = models.Comment.objects.get(pk=comment.pid.id).username
            else:
                data['pid'] = None
                data['fu_username'] = None
            data['pk'] = comment.pk
            data['content'] = comment.content
            data['username'] = comment.username
            data['add_time'] = comment.add_time.strftime('%Y-%m-%d %H:%M:%S')
            data['qq_url'] = f'http://q.qlogo.cn/headimg_dl?dst_uin={comment.qq_email[:-7]}&spec=640&img_type=jpg'

            msg.append(data)
        return msg


# 关于我
class About(View):

    def get(self, request):
        # 文章分类
        categories = models.Category.objects.all()
        # 登录的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None
        return render(request, 'about.html', {'categories': categories, 'cur_user_name': cur_user_name, })


# 评论校验modelform
class CommentForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = "__all__"
        # exclude = ['pid', ]


# 评论展示
class CommentView(View):

    def post(self, request):
        msg = {}
        error = {}
        data = {}
        form = CommentForm(request.POST)
        pid = request.POST.get('pid')
        article_id = request.POST.get('article')
        if form.is_valid():
            msg['success'] = True
            # 保存
            # print(form.cleaned_data)
            comment_obj = form.save()
            data['pk'] = comment_obj.pk
            data['content'] = comment_obj.content
            data['username'] = comment_obj.username
            data['add_time'] = comment_obj.add_time.strftime('%Y-%m-%d %H:%M:%S')
            data['qq_url'] = f'http://q.qlogo.cn/headimg_dl?dst_uin={comment_obj.qq_email[:-7]}&spec=640&img_type=jpg'

            # print(comment_obj.pid)
            # # 评论成功，发送邮件提醒
            #             # article_obj = models.Article.objects.filter(pk=article_id).first()
            #             # send_mail(
            #             #     f'您的{article_obj.title}文章被{comment_obj.username}评论',
            #             #     comment_obj.content,
            #             #     settings.EMAIL_HOST_USER,
            #             #     ["1959013723@qq.com",],  # 文章作者邮箱
            #             # )
            if comment_obj.pid != None:
                # pid = int(comment_obj.pid)

                fu = models.Comment.objects.get(pk=pid).username
                # print(fu)
                data['fu_username'] = fu
            else:
                data['fu_username'] = 0
            msg['data'] = data

        else:
            # print(form.errors)
            msg['success'] = False
            for field in form.fields.keys():
                if form.has_error(field):
                    error[field] = 'valied'
                else:
                    error[field] = 0
            msg['error'] = error
        # print(msg) # 发给AjaxForm的数据
        return JsonResponse(msg)


# class CommentTreeView(View):
#
#     def get(self, request):
#         msg = []
#         article_id = request.GET.get('article_id')
#         # 该文章的所有评论
#         comment_obj = models.Comment.objects.filter(article_id=article_id)
#         for comment in comment_obj:
#             data = {}
#             if comment.pid:
#                 data['pid'] = comment.pid.id
#                 data['fu_username'] = models.Comment.objects.get(pk=comment.pid.id).username
#             else:
#                 data['pid'] = None
#                 data['fu_username'] = None
#             data['pk'] = comment.pk
#             data['content'] = comment.content
#             data['username'] = comment.username
#             data['add_time'] = comment.add_time.strftime('%Y-%m-%d %H:%M:%S')
#             msg.append(data)
#         # print(msg)  # 发给Ajax的数据
#
#         return JsonResponse(msg, safe=False)


class LoginView(View):

    def get(self, request):
        # 文章分类
        categories = models.Category.objects.all()
        # 登录的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None

        return render(request, 'login.html', {'cur_user_name': cur_user_name, 'categories': categories, })

    def post(self, request):
        # 初始化返回值
        res = {"code":500}

        user = request.POST.get('username')
        pwd = request.POST.get('password')
        # 判断用户名和密码
        user_obj = models.UserInfo.objects.filter(username=user, password=set_md5(pwd)).first()
        if user_obj:
            res['code'] = 200
            # 把当前用户id添加到session中
            request.session['user_id'] = user_obj.id

        return JsonResponse(res)



# 登出
class LogoutView(View):

    def get(self, request):
        request.session.flush()  # 清楚所有的cookie和session
        return redirect('index')

# 自定义验证规则
def email_validate(value):
    email_re = re.compile(r'(.*)@(.*).com$')
    if not email_re.match(value):
        raise ValidationError('邮箱格式错误')  # 自定义验证规则的时候，如果不符合你的规则，需要自己发起错误


# 注册验证
class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=6,
        label='用户名',
        widget=forms.widgets.TextInput(attrs={'class': 'username', 'autocomplete': 'off', 'placeholder': '用户名', }),
        error_messages={
            'required': '用户名不能为空！',
            'max_length': '用户名不能大于16位！',
            'min_length': '用户名不能小于6位！',
        }
    )

    password = forms.CharField(
        max_length=32,
        min_length=6,
        label='密码',
        widget=forms.widgets.PasswordInput(attrs={'class': 'password', 'placeholder': '密码', 'oncontextmenu': 'return false', 'onpaste': 'return false', }),
        error_messages={
            'required': '密码不能为空！',
            'max_length': '密码不能大于16位！',
            'min_length': '密码不能小于6位！',
        }
    )

    r_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(attrs={'class': 'password', 'placeholder': '请再次输入密码', }),
        error_messages={
            'required': '密码不能为空！',
        }
    )

    # 全局钩子
    def clean(self):
        values = self.cleaned_data
        r_password = values.get('r_password')
        password = values.get('password')
        if password == r_password:
            return values
        else:
            self.add_error('r_password', '两次输入的密码不一致！')

    email = forms.EmailField(
        label='邮箱',
        error_messages={
            'invalid': '邮箱格式不对！',
            'required': '邮箱不能为空！',
        },
        widget=forms.widgets.EmailInput(attrs={'class': 'email', 'placeholder': '输入邮箱地址', 'type': 'email'}),
        validators=[email_validate, ],
    )


# 注册
class RegisterView(View):

    def get(self, request):
        # 文章分类
        categories = models.Category.objects.all()
        # 登录的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None

        return render(request, 'register.html', {'cur_user_name': cur_user_name, 'categories': categories, })

    def post(self, request):
        res = {"code": 500, "error": None}
        print(request.POST.get('r_password'))
        register_form_obj = RegisterForm(request.POST)
        if register_form_obj.is_valid():
            res['code'] = 200
            print(register_form_obj.cleaned_data)
            register_form_obj.cleaned_data.pop('r_password')
            password = register_form_obj.cleaned_data.pop('password')
            password = set_md5(password)
            register_form_obj.cleaned_data.update({'password': password})
            models.UserInfo.objects.create(
                **register_form_obj.cleaned_data
            )
        else:
            res['error'] = register_form_obj.errors
            print(register_form_obj.errors)


        return JsonResponse(res)