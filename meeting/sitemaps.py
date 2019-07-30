from django.contrib import sitemaps
from django.urls import reverse


class MeetingViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return ['index', 'slot_aviable']

    def location(self, item):
        return reverse(item)
