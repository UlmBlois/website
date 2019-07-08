from django.urls import path
from . import views

urlpatterns = [
    path('singup', views.SignUpView.as_view(), name='signup'),
    path('accounts/<int:pk>/delete', views.DeleteUser.as_view(),
         name='delete_user'),

]
