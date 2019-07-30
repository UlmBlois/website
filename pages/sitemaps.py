from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'yearly'
    protocol = 'https'

    def items(self):
        return ['pilot_informations', 'about', 'contact', 'on_site',
                'terms', 'privacy', 'copyright']

    def location(self, item):
        return reverse(item)
