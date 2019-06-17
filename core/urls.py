from django.urls import path
from . import views

urlpatterns = [
    path('singup', views.signup, name='signup'),
    path('accounts/<int:pk>/delete', views.DeleteUser.as_view(),
         name='delete_user'),

]
