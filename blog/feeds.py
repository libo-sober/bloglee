from django.contrib.syndication.views import Feed
from django.urls import reverse
from blog.models import Article

class BlogRssFeed(Feed):

    title = "大聪明的博客小屋"
    # 描述
    description = '一个用来分享程序员技术的个人博客'
    link = "/rss/"
    def items(self):
        return Article.objects.all()
    def item_title(self, item):
        return item.title
    def get_image_url(self, url):
        return self.request.build_absolute_uri('/image{}'.format(url))
    def item_description(self, item):
        return item.content
    def item_link(self, item):
        return reverse('detail', args=[item.en_us,])