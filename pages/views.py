from django.views.generic.base import TemplateView


class PilotInformationsView(TemplateView):
    template_name = 'pilot_informations.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class OnSiteView(TemplateView):
    template_name = 'on_site.html'
