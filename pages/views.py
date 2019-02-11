from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from pages.models import Topic


class PilotInformationsView(TemplateView):
    template_name = 'pilot_informations.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class OnSiteView(TemplateView):
    template_name = 'on_site.html'


class FAQView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'faq.html'
