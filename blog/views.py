import datetime
import mistune

from django.shortcuts import render
from django.views.generic.base import View
from blog import models
from BlogLee import settings
from blog.utils.page_html import MyPagination

# Create your views here.
time = datetime.datetime(year=2099, month=1, day=1)

class Index(View):

    def get(self, request):
        """首页展示"""

        page_id = request.GET.get('page')  # 获取get请求中的page数据
        num = models.Article.objects.all().count()  # 总共记录数
        base_url = request.path  # 请求路径
        get_data = request.GET.copy()  # 直接调用这个类自己的copy方法或者deepcopy方法或者自己import copy 都可以实现内容允许修改
        models.Article.objects.filter(is_recommend=1).update(add_time=time)  # <QuerySet [<Article: 太黑的诱惑>]>
        all_articles = models.Article.objects.all().order_by('-add_time')  # <QuerySet [<Article: 333>]>
        # 以后直接在settings配置文件中修改即可
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录
        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count, record=record)
        # all_articles = articles | top_articles  # 合并两个queryset
        all_articles = all_articles[
                       (html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]

        # 文章分类
        categories = models.Category.objects.all()

        return render(request, 'index.html', {'all_articles': all_articles, 'page_html': html_obj.html_page(), 'categories': categories, })


class ArticleView(View):

    def get(self, request, article_id=None):
        article = models.Article.objects.get(pk=article_id)
        article.viewed()  # 增加阅读数
        mk = mistune.Markdown()
        output = mk(article.content)

        # 文章分类
        categories = models.Category.objects.all()

        return render(request, 'datail.html', {'article': article, 'detail_html': output, 'categories': categories,})


class CategoryView(View):

    def get(self, request, cid):
        # 文章分类
        categories = models.Category.objects.all()
        # categoriy_id对应类下的所有文章
        models.Article.objects.filter(is_recommend=1).update(add_time=time)
        all_articles = models.Article.objects.filter(category_id=cid).order_by('-add_time')

        return render(request, 'category.html', {'categories': categories, 'all_articles': all_articles, })

# 关于我
class About(View):

    def get(self, request):
        return render(request, 'about.html')