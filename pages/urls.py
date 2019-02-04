from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('pages/PilotInformations', views.PilotInformationsView.as_view(),
         name='pilot_informations')
]
