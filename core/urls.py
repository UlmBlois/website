from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('singup', views.signup, name='signup'),
    url(r'^user/(?P<pk>\d+)/edit/$', views.UpdateUser.as_view(),
        name='edit_user'),
]
