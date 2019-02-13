from django.urls import path
from django.conf.urls import url
from . import views
from meeting.filters import ReservationFilter


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^pilot/password/$', views.pilot_change_password,
        name='change_password'),
    path('pilot/<int:pk>/detail/', views.DetailPilot.as_view(), name='pilot'),
    url(r'^pilot/(?P<pk>\d+)/edit/$', views.UpdateUserPilotView.as_view(),
        name='edit_pilot'),
    path('ulm/', views.PilotULMList.as_view(),
         name='pilot_ulm_list'),
    path('ulm/<int:pk>/delete/', views.DeletePilotULM.as_view(),
         name='pilot_delete_ulm'),
    path('ulm/<int:pk>/edit/', views.UpdatePilotULM.as_view(),
         name='pilot_update_ulm'),
    path('ulm/new/', views.CreatePilotULM.as_view(),
         name='pilot_create_ulm'),
    path('reservation', views.PilotReservationList.as_view(),
         name='pilot_reservation'),
    path('reservation/new', views.CreatePilotReservation.as_view(),
         name='pilot_create_reservation'),
    path('reservation/<int:pk>/edit/', views.UpdatePilotReservation.as_view(),
         name='pilot_update_reservation'),
    path('reservation/<int:pk>/delete/',
         views.DeletePilotReservation.as_view(),
         name='pilot_delete_reservation'),
]


# STAFF url
urlpatterns += [
    path('staff/fuel/', views.FilteredReservationList.as_view(
         filterset_class=ReservationFilter,
         template_name='staff_fuel_reservation_list.html'),
         name="staff_fuel_res_list"),
    path('staff/reservation/', views.FilteredReservationList.as_view(
        filterset_class=ReservationFilter,
        template_name='staff_reservation_list.html'),
        name='staff_reservation_list'),
]


# AJAX url
urlpatterns += [
    path('ajax/reservation/fuelserved/<int:pk>/', views.ajax_fuel_served,
         name="ajax_fuel_served"),
    path('ajax/load_ulm/', views.ajax_load_pilot_ulm_list,
         name="ajax_ulm_option_list"),
    path('ajax/add_ulm/<int:pk>/', views.ajax_add_ulm, name="ajax_add_ulm"),
    path('staff/reservation/<int:pk>/edit/',
         views.ajax_staff_edit_reservation,
         name="staff_edit_reservation"),

]