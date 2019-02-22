from django.urls import path
from django.conf.urls import url
from . import views
from meeting.filters import ReservationFilter


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^pilot/password/$', views.pilot_change_password,
        name='change_password'),
    path('pilot/<int:pk>/detail/', views.DetailPilot.as_view(), name='pilot'),
    path('pilot/<int:pk>/edit/', views.UpdateUserPilotView.as_view(),
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
    path('staff/reservation/validation/<int:pk>/overview/',
         views.StaffReservationValidationDetail.as_view(),
         name='staff_reservation_overview'),
    path('staff/reservation/validation/<int:res>/edit/pilot/<int:pk>',
         views.StaffReservationUpdatePilot.as_view(),
         name='staff_reservation_edit_pilot'),
    path('staff/reservation/validation/<int:res>/edit/ulm/<int:pk>',
         views.StaffReservationUpdatePilotULM.as_view(),
         name='staff_reservation_edit_ulm'),
    path('staff/reservation/validate/edit/<int:pk>',
         views.StaffReservationUpdate.as_view(),
         name='staff_reservation_edit'),
    path('staff/reservation/validation/<int:pk>/validate/',
         views.StaffReservationValidation.as_view(),
         name="staff_reservation_validate"),
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
