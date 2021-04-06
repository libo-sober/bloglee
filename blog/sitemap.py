from django.contrib.sitemaps import Sitemap
from blog.models import Article, Category, Tag, UserInfo
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'friends', 'about', 'archive', 'messages']

    def location(self, item):
        return reverse(item)


class ArticleSiteMap(Sitemap):
    changefreq = "Weekly"
    priority = "0.6"

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.update_time


class CategorySiteMap(Sitemap):
    changefreq = "Weekly"
    priority = "0.6"

    def items(self):
        return Category.objects.all()

    # def lastmod(self, obj):
    #     return obj.last_mod_time


class TagSiteMap(Sitemap):
    changefreq = "Weekly"
    priority = "0.3"

    def items(self):
        return Tag.objects.all()

    # def lastmod(self, obj):
    #     return obj.last_mod_time


# class UserSiteMap(Sitemap):
#     changefreq = "Weekly"
#     priority = "0.3"
#
#     def items(self):
#         return UserInfo.objects.all()
#
#     def lastmod(self, obj):
#         return obj.date_joined