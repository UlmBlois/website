from django.urls import path
from . import views

urlpatterns = [
    path('', views.FAQView.as_view(), name='faq'),
]
