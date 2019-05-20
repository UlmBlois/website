from django.urls import path
from . import views

urlpatterns = [
    path('PilotInformations', views.PilotInformationsView.as_view(),
         name='pilot_informations'),
    path('About', views.AboutView.as_view(), name='about'),
    path('Contact', views.ContactView.as_view(), name='contact'),
    path('on_site', views.OnSiteView.as_view(), name='on_site'),
]
