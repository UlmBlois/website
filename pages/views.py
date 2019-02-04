from django.shortcuts import render
from django.views.generic.base import TemplateView


class PilotInformationsView(TemplateView):
    template_name = 'pilot_informations.html'
