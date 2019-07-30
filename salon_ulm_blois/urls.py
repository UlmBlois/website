"""ulm_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap

from core.form import PasswordResetForm
from pages.sitemaps import StaticViewSitemap
from core.sitemaps import CoreViewSitemap
from faq.sitemaps import FaqViewSitemap
from meeting.sitemaps import MeetingViewSitemap
# TODO: DEBUG ONLY
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'core.views.handler_404'
handler500 = 'core.views.handler_500'
handler403 = 'core.views.handler_403'
handler400 = 'core.views.handler_400'

sitemaps = {
    'static': StaticViewSitemap,
    'core': CoreViewSitemap,
    'faq': FaqViewSitemap,
    'meeting': MeetingViewSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(
            form_class=PasswordResetForm,
            html_email_template_name='password_reset_email.html'),
         name="password_reset"),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('meeting/', include('meeting.urls')),
    path('pages/', include('pages.urls')),
    path('faq/', include('faq.urls')),
    path('', RedirectView.as_view(url='/meeting/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    url(r'^tinymce/', include('tinymce.urls')),
]
