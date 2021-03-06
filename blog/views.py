import datetime
import mistune
import re
import html

from django.core.exceptions import ValidationError
from django import forms
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.base import View
from blog import models
from blog.utils.page_html import MyPagination
from blog.utils.email_validation import random_str
from django.core.mail import send_mail
from BlogLee import settings
from blog.utils.hashlib_func import set_md5
from django.db.models import Q
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html as phtml
class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = phtml.HtmlFormatter()
        return highlight(code, lexer, formatter)

# Create your views here.
time = datetime.datetime(year=2099, month=1, day=1)


class Index(View):

    def get(self, request, en_us_c=None, en_us_tag=None):
        """首页展示"""
        print(en_us_c, en_us_tag)
        cid = en_us_c
        tag_id = en_us_tag
        if en_us_c:
            if en_us_c != 'category':
                c_obj = models.Category.objects.filter(en_us=en_us_c).first()
                cid = c_obj.id
        if en_us_tag:
            tag_obj = models.Tag.objects.filter(en_us=en_us_tag).first()
            tag_id = tag_obj.id


        print(cid, tag_id)
        # 文章对象
        article_obj = models.Article.objects.filter(is_display=False)
        # 评论对象
        comment_obj = models.Comment.objects.all()
        # 文章总数
        article_count = article_obj.count()
        # 评论总数
        comment_count = comment_obj.count()
        page_id = request.GET.get('page')  # 获取get请求中的page数据
        num = models.Article.objects.all().count()  # 总共记录数
        base_url = request.path  # 请求路径
        get_data = request.GET.copy()  # 直接调用这个类自己的copy方法或者deepcopy方法或者自己import copy 都可以实现内容允许修改
        # models.Article.objects.filter(is_recommend=1).update(add_time=time)  # <QuerySet [<Article: 太黑的诱惑>]>
        # all_articles = models.Article.objects.all().order_by('-add_time')  # <QuerySet [<Article: 333>]>
        top_articles = list(article_obj.filter(is_recommend=1).order_by('-add_time'))
        articles = list(article_obj.filter(is_recommend=False).order_by('-add_time'))
        all_articles = top_articles + articles
        # 以后直接在settings配置文件中修改即可
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录
        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count,
                                record=record)
        # all_articles = articles | top_articles  # 合并两个queryset
        all_articles = all_articles[
                       (html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
        # P = models.Article.objects.get(id=8)
        # print(P.get_absolute_url())
        # 文章分类
        categories = models.Category.objects.all()
        # 文章专栏
        columns = models.Column.objects.all().order_by('-weights')

        # 最新文章
        new_articles = article_obj.order_by('-add_time')[:5]
        # 最热文章
        hot_articles = article_obj.order_by('-click_count')[:5]
        # 最新评论
        new_comments = comment_obj.order_by('-add_time')[:5]
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

        if tag_id:
            # tag_id对应类下的所有文章
            obj = models.Article.objects.filter(is_display=False).filter(tag__pk=tag_id)
            tags_num = obj.count() # 总共记录数
            tags_top_articles = list(obj.filter(is_recommend=1).order_by('-add_time'))
            tags_articles = list(obj.filter(is_recommend=False).order_by('-add_time'))
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
                           'qq_url': qq_url, 'admin_obj': admin_obj, 'columns': columns, })

        elif cid:
            # categoriy_id对应类下的所有文章
            categories_obj = models.Article.objects.filter(is_display=False).filter(category_id=cid)
            categories_num = categories_obj.count()  # 总共记录数
            categories_top_articles = list(categories_obj.filter(is_recommend=1).order_by('-add_time'))
            categories_articles = list(categories_obj.filter(is_recommend=False).order_by('-add_time'))
            categories_all_articles = categories_top_articles + categories_articles
            html_obj = MyPagination(page_id=page_id, num=categories_num, base_url=base_url, get_data=get_data,
                                    page_count=page_count, record=record)
            categories_all_articles = categories_all_articles[
                                      (html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
            return render(request, 'category.html',
                          {'categories_all_articles': categories_all_articles, 'page_html': html_obj.html_page(),
                           'categories':
                               categories, 'article_count': article_count, 'comment_count': comment_count,
                           'new_articles': new_articles, 'hot_articles':
                               hot_articles, 'new_comments': new_comments, 'tags': tags, 'cur_user_name': cur_user_name,
                           'qq_url': qq_url, 'admin_obj': admin_obj, 'columns': columns, })
        else:
            return render(request, 'index.html',
                          {'all_articles': all_articles, 'page_html': html_obj.html_page(), 'categories':
                              categories, 'article_count': article_count, 'comment_count': comment_count,
                           'new_articles': new_articles, 'hot_articles':
                               hot_articles, 'new_comments': new_comments, 'tags': tags, 'cur_user_name': cur_user_name,
                           'qq_url': qq_url, 'admin_obj': admin_obj, 'columns': columns, })


# 文章详情页
class ArticleView(View):

    def get(self, request, en_us=None):
        # 上一页下一页
        # print(article_id)
        print(en_us)
        article = models.Article.objects.get(en_us=en_us)
        article_id = article.id
        all_article = models.Article.objects.all()
        previous_index = 0
        next_index = 0
        curr_article = None
        previous_index = 0
        next_index = 0
        previous_article = None
        next_article = None
        print(article_id)
        obj = models.Article.objects.all()
        if obj.count() == 1:
            curr_article = obj.first()
        else:
            for index, article in enumerate(all_article):
                if index == 0:
                    previous_index = 0
                    next_index = index + 1
                elif index == len(all_article) - 1:
                    previous_index = index - 1
                    next_index = index
                else:
                    previous_index = index - 1
                    next_index = index + 1

                # 通过id判断当前记录;
                # 接收的article_id是字符串 对象本身的id是int
                if article.id == int(article_id):
                    curr_article = article
                    previous_article = all_article[previous_index]
                    next_article = all_article[next_index]
                    break
        # article = models.Article.objects.get(pk=article_id)
        # print(curr_article)
        curr_article.viewed()  # 增加阅读数P
        # 为甚么刷新页面会产生两次访问ArticleView
        # 已经解决，因为文章中的请求js或者csss图片等路径为空或出错的，就会自动请求当前路径
        if curr_article.is_md:
            renderer = mistune.Renderer(escape=False, hard_wrap=True)
            mk = mistune.Markdown(renderer=renderer)
            output = mk(curr_article.content)
            print('md')
        else:
            output = curr_article.content
        # 文章分类
        print(output)
        categories = models.Category.objects.all()
        # 文章专栏
        columns = models.Column.objects.all().order_by('-weights')

        # 该文章评论分页
        comment_obj = models.Comment.objects.filter(article_id=article_id).order_by('-add_time')
        page_id = request.GET.get('page')  # 获取get请求中的page数据
        num = comment_obj.count()  # 总共记录数
        base_url = request.path  # 请求路径
        get_data = request.GET.copy()  # 直接调用这个类自己的copy方法或者deepcopy方法或者自己import copy 都可以实现内容允许修改
        # 以后直接在settings配置文件中修改即可
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录
        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count,
                                record=record)
        comment_obj = comment_obj[
                      (html_obj.page_id - 1) * html_obj.record : html_obj.page_id * html_obj.record]
        comment_list = self.build_msg(comment_obj)
        ret = self.get_comment_list(comment_list)

        # 登录的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None

        # 管理员用户对象
        admin_obj = models.UserInfo.objects.filter(is_admin=True).first()

        return render(request, 'datail.html',
                      {'article': curr_article, 'detail_html': output, 'categories': categories, 'ret':
                          ret, 'cur_user_name': cur_user_name, 'columns': columns, 'previous_article': previous_article,
                       'next_article': next_article, 'admin_obj': admin_obj, 'page_html': html_obj.html_page(),})

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
            user_obj = models.UserInfo.objects.filter(username=comment.username).first()
            fu_user_obj = models.UserInfo.objects.filter(username=data['fu_username']).first()
            # print(user_obj)
            if user_obj:
                data['is_admin'] = user_obj.is_admin
                if user_obj.avatar:
                    data['avatar'] = user_obj.avatar.url
                else:
                    data['avatar'] = None

            else:
                data['is_admin'] = False
                data['avatar'] = None

            if fu_user_obj:
                data['fu_is_admin'] = fu_user_obj.is_admin
            else:
                data['fu_is_admin'] = False
            # data['admin_img'] = settings.ADMIN_IMG

            msg.append(data)

        # print(msg)
        return msg


# 关于我
class About(View):

    def get(self, request):
        # 文章分类
        categories = models.Category.objects.all()
        # 文章专栏
        columns = models.Column.objects.all().order_by('-weights')

        # 登录的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None
        admin_obj = models.UserInfo.objects.filter(is_admin=True).first()
        url = admin_obj.avatar.url

        about = models.About.objects.all().first()

        return render(request, 'about.html',
                      {'categories': categories, 'cur_user_name': cur_user_name, 'columns': columns, 'url': url,
                       'about': about, })


# 自定义验证规则
def email_validate(value):
    email_re = re.compile(r'\w{5,12}@(.*).com$')
    if not email_re.match(value):
        raise ValidationError('邮箱格式错误')  # 自定义验证规则的时候，如果不符合你的规则，需要自己发起错误
    else:
        return value


# 评论校验modelform
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = "__all__"
        # exclude = ['pid', ]
        error_messages = {
            'username': {
                'required': '昵称不能为空！',
                'invalid': '用户名错误',
            },
            'qq_email': {
                'required': '邮箱不能为空！',
                'invalid': '邮箱格式错误',
            },
            'content': {
                'required': '内容不能为空！',
                'invalid': '内容错误',
            },
        }

    def clean_username(self):

        username = self.cleaned_data['username']
        user_obj = models.UserInfo.objects.filter(username=username).first()
        if user_obj:
            raise forms.ValidationError('昵称已存在！')
        else:
            return username

    def clean_qq_email(self):
        qq_email = self.cleaned_data['qq_email']
        # print(qq_email)
        return email_validate(qq_email)


# 评论添加
class CommentView(View):

    def post(self, request):
        msg = {}
        error = {}
        data = {}
        form = CommentForm(request.POST)
        pid = request.POST.get('pid')
        # 如果已经登录则不用校验‘
        user_id = request.session.get('user_id')
        if user_id:
            msg['success'] = True
            username = request.POST.get('username')
            content = request.POST.get('content')
            # 防止js注入
            re_script = re.compile(r'<script>(.*?)</script>')
            re_js = re.compile(r'javascript')
            if re_script.search(content) or re_js.search(content):
                content = html.escape(content)
            article = request.POST.get('article')
            qq_email = request.POST.get('qq_email')
            web_site = request.POST.get('web_site')
            pid = request.POST.get('pid')
            models.Article.objects.get(id=article).commented()

            comment_obj = models.Comment.objects.create(
                username=username,
                content=content,
                qq_email=qq_email,
                article=models.Article.objects.get(id=article),
                web_site=web_site,
                pid=models.Comment.objects.filter(id=pid).first(),
            )
            data['pk'] = comment_obj.pk
            data['content'] = comment_obj.content
            data['username'] = comment_obj.username
            data['add_time'] = comment_obj.add_time.strftime('%Y-%m-%d %H:%M:%S')
            data['qq_url'] = f'http://q.qlogo.cn/headimg_dl?dst_uin={comment_obj.qq_email[:-7]}&spec=640&img_type=jpg'

            # print(comment_obj.pid)
            # 评论成功，发送邮件提醒
            article_obj = models.Article.objects.filter(pk=article).first()
            email_content = f"评论人：{username}\n评论文章：{article_obj.title}\n评论时间：{data['add_time']}\n" \
                            f"评论人邮箱：{qq_email}\n评论内容：{comment_obj.content}\n"
            send_mail(
                f'您的{article_obj.title}文章被{comment_obj.username}评论',
                email_content,
                settings.EMAIL_HOST_USER,
                ["libo_sober@163.com",],  # 文章作者邮箱
            )
            if comment_obj.pid != None:
                # pid = int(comment_obj.pid)

                fu = models.Comment.objects.get(pk=pid).username
                # print(fu)
                data['fu_username'] = fu
            else:
                data['fu_username'] = 0
            msg['data'] = data
            # msg['error'] = None
        else:

            # msg['success'] = False
            # msg['error'] = {'login':'为防止匿名攻击，请登录验证邮箱！'}
            qq_email = request.POST.get('qq_email')
            if form.is_valid():
                msg['success'] = True
                article = request.POST.get('article')
                models.Article.objects.get(id=article).commented()
                # 保存
                content = form.cleaned_data.pop('content')
                username = form.cleaned_data.pop('username')
                username = html.escape(username)
                # 防止js注入
                # 陌生人全部防止js注入
                re_script = re.compile(r'<script>(.*?)</script>')
                re_js = re.compile(r'javascript')
                if re_script.search(content) or re_js.search(content):
                    content = html.escape(content)
                # content = html.escape(content)
                form.cleaned_data.update({'content': content})
                form.cleaned_data.update({'username': username})
                comment_obj = models.Comment.objects.create(
                    **form.cleaned_data
                )
                data['pk'] = comment_obj.pk
                data['content'] = comment_obj.content
                data['username'] = comment_obj.username
                data['add_time'] = comment_obj.add_time.strftime('%Y-%m-%d %H:%M:%S')
                data['qq_url'] = f'http://q.qlogo.cn/headimg_dl?dst_uin={comment_obj.qq_email[:-7]}&spec=640&img_type=jpg'

                print(comment_obj.pid)
                # 评论成功，发送邮件提醒
                article_id = int(comment_obj.article_id)
                article_obj = models.Article.objects.filter(pk=article_id).first()
                email_content = f"评论人：{data['username']}\n评论文章：{article_obj.title}\n评论时间：{data['add_time']}\n" \
                                f"评论人邮箱：{qq_email}\n评论内容：{comment_obj.content}\n"
                # send_mail(
                #     f'您的{article_obj.title}文章被{comment_obj.username}评论',
                #     email_content,
                #     settings.EMAIL_HOST_USER,
                #     ["libo_sober@163.com",],  # 文章作者邮箱
                # )
                if comment_obj.pid != None:
                    # pid = int(comment_obj.pid)

                    fu = models.Comment.objects.get(pk=pid).username
                    # print(fu)
                    data['fu_username'] = fu
                else:
                    data['fu_username'] = 0
                msg['data'] = data

            else:
                msg['success'] = False
                msg['error'] = form.errors
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
        # 文章专栏
        columns = models.Column.objects.all().order_by('-weights')

        # 登录的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None

        return render(request, 'login.html',
                      {'cur_user_name': cur_user_name, 'categories': categories, 'columns': columns, })

    def post(self, request):
        # 初始化返回值
        res = {"code": 500, 'errors':''}

        user = request.POST.get('username')
        pwd = request.POST.get('password')
        # 判断用户名和密码
        user_obj_set = models.UserInfo.objects.filter(username=user, password=set_md5(pwd))
        user_obj = user_obj_set.first()
        print(user_obj)
        if user_obj:

            if user_obj.is_active:
                res['code'] = 200
                # 更新最后登录时间
                user_obj_set.update(last_login=datetime.datetime.now())
                # 把当前用户id添加到session中
                request.session['user_id'] = user_obj.id
            else:
                res['errors'] = {'active': '请先去您的邮箱激活账户！'}

        else:
            res['errors'] = {'userpwd': '用户名或密码错误！！'}

        return JsonResponse(res)


# 登出
class LogoutView(View):

    def get(self, request):
        request.session.flush()  # 清楚所有的cookie和session
        return redirect('login')


# 注册验证
class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=3,
        label='用户名',
        error_messages={
            'required': '用户名不能为空！',
            'max_length': '用户名不能大于16位！',
            'min_length': '用户名不能小于3位！',
        }
    )

    password = forms.CharField(
        max_length=32,
        min_length=6,
        label='密码',
        error_messages={
            'required': '密码不能为空！',
            'max_length': '密码不能大于16位！',
            'min_length': '密码不能小于6位！',
        }
    )

    r_password = forms.CharField(
        label='确认密码',
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

    # 局部钩子
    def clean_username(self):
        values = self.cleaned_data
        username = values.get('username')
        user_obj = models.UserInfo.objects.filter(username=username)
        if user_obj:
            self.add_error('username', '用户名已存在！')
        else:
            return username

    email = forms.EmailField(
        label='邮箱',
        error_messages={
            'invalid': '邮箱格式不对！',
            'required': '邮箱不能为空！',
        },
        validators=[email_validate, ],
    )


# 注册
class RegisterView(View):

    def get(self, request):
        # 文章分类
        categories = models.Category.objects.all()
        # 文章专栏
        columns = models.Column.objects.all().order_by('-weights')

        # 登录的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None

        return render(request, 'register.html',
                      {'cur_user_name': cur_user_name, 'categories': categories, 'columns': columns, })

    def post(self, request):
        res = {"code": 500, "error": None}
        # print(request.POST.get('r_password'))
        register_form_obj = RegisterForm(request.POST)
        print(request.POST.get('username'))
        if register_form_obj.is_valid():
            res['code'] = 200
            print(register_form_obj.cleaned_data)
            register_form_obj.cleaned_data.pop('r_password')
            password_ = register_form_obj.cleaned_data.pop('password')
            password = set_md5(password_)
            register_form_obj.cleaned_data.update({'password': password})
            models.UserInfo.objects.create(
                **register_form_obj.cleaned_data
            )
            username = register_form_obj.cleaned_data['username']
            email = register_form_obj.cleaned_data['email']
            code = random_str(16)
            # print(code)
            # 注册成功，发送邮件激活
            models.EmailVerifyRecord.objects.create(
                code=code,
                email=email,
            )
            email_content = f'该邮件为大聪明博客网站用户激活邮件，如果不是您本人操作请勿点击。\n用户名：{username}\n' \
                            f'密码：{password_}\n请点击下面的链接激活你的账号:https://liboer.top/activation/{code}\n' \
                            f'若跳转到登录页面则成功激活\n' \
                            f'若跳转到注册页面则激活失败\n'
            print(email_content)
            # send_mail(
            #     f'大聪明博客用户：{username}的激活链接',
            #     email_content,
            #     settings.EMAIL_FROM,
            #     [email, ],  # 文章作者邮箱
            # )
        else:
            res['error'] = register_form_obj.errors
            # print(register_form_obj.errors)

        return JsonResponse(res)


class Activate(View):
    def get(self, request, active_code):
        print(active_code)
        code_obj = models.EmailVerifyRecord.objects.filter(code=active_code).first()
        if code_obj:
            models.UserInfo.objects.filter(email=code_obj.email).update(is_active=True)
            return redirect('login')
        else:
            return redirect('register')

def page_not_found(request, exception):
    # 文章分类
    categories = models.Category.objects.all()
    # 文章专栏
    columns = models.Column.objects.all().order_by('-weights')

    # 登录的用户对象
    user_id = request.session.get('user_id')
    if user_id:
        cur_user_name = models.UserInfo.objects.get(id=user_id)
    else:
        cur_user_name = None

    return render(request, '404.html', {'cur_user_name': cur_user_name, "categories": categories, 'columns': columns, })


class UserInfoView(View):

    def get(self, request):
        # 文章分类
        categories = models.Category.objects.all()
        # 文章专栏
        columns = models.Column.objects.all().order_by('-weights')

        # 登录的用户对象
        user_id = request.session.get('user_id')

        cur_user_name = models.UserInfo.objects.get(id=user_id)

        return render(request, 'userinfo.html',
                      {'cur_user_name': cur_user_name, "categories": categories, 'columns': columns, })

    def post(self, request):

        # 登录的用户对象
        user_id = request.session.get('user_id')
        uname = models.UserInfo.objects.get(id=user_id).username

        msg = {'code': 500, 'error': None}
        username = request.POST.get('username')
        user_obj = models.UserInfo.objects.filter(~Q(id=user_id)).filter(username=username)
        if user_obj:
            msg['error'] = {'username': '用户名已经存在！'}
        else:
            msg['code'] = 200
            avatar_obj = request.FILES.get('avatar')
            print(avatar_obj)
            if avatar_obj:
                path = 'uploads' + '/' + 'avatars' + '/' + avatar_obj.name
                with open(path, mode='wb') as fp:
                    for img in avatar_obj:
                        fp.write(img)
                url = 'avatars' + '/' + avatar_obj.name
                models.UserInfo.objects.filter(id=user_id).update(avatar=url)
            models.Comment.objects.filter(username=uname).update(username=uname)
            models.UserInfo.objects.filter(id=user_id).update(username=uname)
        return JsonResponse(msg)


class ModifyView(View):

    def post(self, request):
        msg = {'code': 500, 'error': None}
        # 登录的用户对象
        user_id = request.session.get('user_id')
        # cur_user_name = models.UserInfo.objects.get(id=user_id)
        # print(user_id)
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        # print(old_password)
        if models.UserInfo.objects.get(id=user_id).password == set_md5(old_password):
            msg['code'] = 200
            models.UserInfo.objects.filter(id=user_id).update(password=set_md5(new_password))
        else:
            error = {'password': '原密码不正确！'}
            msg['error'] = error
        return JsonResponse(msg)


class ArchiveView(View):

    def get(self, request):
        user_id = request.session.get('user_id')
        # 文章分类
        categories = models.Category.objects.all()
        # 文章专栏
        columns = models.Column.objects.all().order_by('-weights')

        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None

        dates = models.Article.objects.datetimes('add_time', 'month', order='DESC')

        return render(request, 'archive.html',
                      {'cur_user_name': cur_user_name, "categories": categories, 'columns': columns, 'dates': dates, })


class FriendsForm(forms.ModelForm):
    class Meta:
        model = models.Links
        fields = "__all__"
        error_messages = {
            'title': {
                'required': '昵称不能为空！',
                'invalid': '用户名错误',
            },
            'url': {
                'required': '地址不能为空！',
                'invalid': '地址格式错误',
            },
            'image': {
                'required': '头像不能为空！',
                'invalid': '头像格式错误',
            },
        }


class FriendsView(View):

    def get(self, request):

        user_id = request.session.get('user_id')
        # 文章分类
        categories = models.Category.objects.all()
        # 文章专栏
        columns = models.Column.objects.all().order_by('-weights')
        for col in columns:
            print(col.icon)

        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None

        frieds_obj = models.Links.objects.filter(is_disply=True)

        return render(request, 'friends.html',
                      {'cur_user_name': cur_user_name, "categories": categories, 'columns': columns,
                       'frieds_obj': frieds_obj, })

    def post(self, request):
        msg = {'code': 500, 'error': None}
        form = FriendsForm(request.POST)
        # 登录的用户对象
        user_id = request.session.get('user_id')
        if user_id:
            uesr_obj = models.UserInfo.objects.get(id=user_id)
            if form.is_valid():
                print(form.cleaned_data)
                msg['code'] = 200
                form.save()
                title = form.cleaned_data['title']
                url = form.cleaned_data['url']
                image = form.cleaned_data['image']
                desc = form.data['desc']
                name = uesr_obj.username
                email = uesr_obj.email
                print(desc)
                content = f'{name}请求友情链接，他的邮箱：{email}\n详细信息：\ntitle:{title}\nurl:{url}\nimage:{image}\ndesc:{desc}\n'
                # 评论成功，发送邮件提醒
                send_mail(
                    f'{name}向你申请友情链接',
                    content,
                    settings.EMAIL_HOST_USER,
                    ["libo_sober@163.com", ],  # 文章作者邮箱
                )
            else:
                msg['error'] = form.errors
        else:
            msg['error'] = {'login': '请先登录！'}

        return JsonResponse(msg)


class MessagesView(View):

    def get(self, request):

        user_id = request.session.get('user_id')
        # 文章分类
        categories = models.Category.objects.all()
        # 文章专栏
        columns = models.Column.objects.all().order_by('-weights')

        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None

        least_users = models.UserInfo.objects.all().order_by('-last_login')[:20]
        # for user in least_users:
        #     if user.avatar is None:
        # url = f'http://q.qlogo.cn/headimg_dl?dst_uin={user.email[:-7]}&spec=640&img_type=jpg'

        # 所有评论
        page_id = request.GET.get('page')  # 获取get请求中的page数据
        num = models.Comment.objects.all().count()  # 总共记录数
        base_url = request.path  # 请求路径
        get_data = request.GET.copy()  # 直接调用这个类自己的copy方法或者deepcopy方法或者自己import copy 都可以实现内容允许修改
        # 以后直接在settings配置文件中修改即可
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录
        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count,
                                record=record)
        article_id = 23
        comment_obj = models.Comment.objects.filter(article_id=article_id).order_by('-add_time')
        comment_obj = comment_obj[
                       (html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
        comment_list = self.build_msg(comment_obj)
        ret = self.get_comment_list(comment_list)

        return render(request, 'messages.html',
                      {'cur_user_name': cur_user_name, "categories": categories, 'columns': columns,
                       'least_users': least_users, 'ret': ret, 'page_html': html_obj.html_page(),})

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
            user_obj = models.UserInfo.objects.filter(username=comment.username).first()
            fu_user_obj = models.UserInfo.objects.filter(username=data['fu_username']).first()
            # print(user_obj)
            if user_obj:
                data['is_admin'] = user_obj.is_admin
                if user_obj.avatar:
                    data['avatar'] = user_obj.avatar.url
                else:
                    data['avatar'] = None

            else:
                data['is_admin'] = False
                data['avatar'] = None
            if fu_user_obj:
                data['fu_is_admin'] = fu_user_obj.is_admin
            else:
                data['fu_is_admin'] = False
            # data['admin_img'] = settings.ADMIN_IMG

            msg.append(data)
        return msg


class LoveView(View):

    def get(self, request):
        msg = {}
        msg['status'] = 'success'
        id = request.GET.get('id')
        models.Article.objects.get(id=id).upuped()

        return JsonResponse(msg)


class SearchView(View):

    def get(self, request):

        # 文章总数
        article_count = models.Article.objects.count()
        # 评论总数
        comment_count = models.Comment.objects.count()
        page_id = request.GET.get('page')  # 获取get请求中的page数据
        base_url = request.path  # 请求路径
        get_data = request.GET.copy()  # 直接调用这个类自己的copy方法或者deepcopy方法或者自己import copy 都可以实现内容允许修改
        # 以后直接在settings配置文件中修改即可
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录

        # 文章分类
        categories = models.Category.objects.all()
        # 文章专栏
        columns = models.Column.objects.all().order_by('-weights')

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

        q = request.GET.get('q')
        if q:
            search_all_articles = models.Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).order_by('-add_time')
            num = len(search_all_articles)
            html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data,
                                    page_count=page_count,
                                    record=record)
            search_all_articles = search_all_articles[
                           (html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
            return render(request, 'search.html',
                          {'all_articles': search_all_articles, 'page_html': html_obj.html_page(),
                           'categories':
                               categories, 'article_count': article_count, 'comment_count': comment_count,
                           'new_articles': new_articles, 'hot_articles':
                               hot_articles, 'new_comments': new_comments, 'tags': tags, 'cur_user_name': cur_user_name,
                           'qq_url': qq_url, 'admin_obj': admin_obj, 'columns': columns, })


        else:
            return redirect('index')
