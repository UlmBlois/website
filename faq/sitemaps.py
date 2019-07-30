from django.contrib import sitemaps
from django.urls import reverse


class FaqViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return ['faq']

    def location(self, item):
        return reverse(item)
