from django.contrib import sitemaps
from django.urls import reverse


class CoreViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'yearly'
    protocol = 'https'

    def items(self):
        return []

    def location(self, item):
        return reverse(item)
