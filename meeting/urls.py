from django.urls import path
from . import views
from meeting import filters


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('pilot/password/', views.PilotChangePassword.as_view(),
         name='change_password'),
    path('pilot/<int:pk>/detail/', views.DetailPilot.as_view(), name='pilot'),
    path('pilot/<int:pk>/edit/', views.UpdateUserPilotView.as_view(),
         name='edit_pilot'),
    path('pilot/', views.LoggedIndexView.as_view(), name='logged_index'),
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
    path('reservation/<int:pk>/edit', views.UpdatePilotReservation.as_view(),
         name='pilot_update_reservation'),
    path('reservation/wizard/<int:pk>/user',
         views.ReservationWizardStep1.as_view(),
         name='reservation_wizard_step1'),
    path('reservation/wizard/<int:pilot>/ulm',
         views.ReservationWizardStep2.as_view(),
         name='reservation_wizard_step2'),
    path('slot/aviable',
         views.TimeSlotAviableView.as_view(),
         name='slot_aviable'),
]


# STAFF url
urlpatterns += [
    path('staff/pilot/<int:pilot>/edit/ulm/<int:pk>/',
         views.StaffUpdatePilotULM.as_view(),
         name='staff_update_ulm'),
    path('staff/pilot/<int:pilot>/edit/reservation/<int:pk>',
         views.StaffUpdatePilotReservation.as_view(),
         name='staff_update_reservation'),
    path('staff/pilot/<int:pk>/edit/profile/',
         views.StaffUpdatePilot.as_view(),
         name="staff_update_pilot"),
    path('staff/pilot/<int:pk>/overview/', views.PilotOverview.as_view(),
         name='pilot_overview'),
    path('staff/ulm/', views.FilteredULMList.as_view(
        filterset_class=filters.ULMFilter,
        template_name='staff_ulm_list.html'),
        name='staff_ulm_list'),
    path('staff/pilot/', views.FilteredPilotList.as_view(
        filterset_class=filters.PilotFilter,
        template_name='staff_pilot_list.html'),
        name='staff_pilot_list'),
    path('staff/fuel/', views.FilteredReservationList.as_view(
         filterset_class=filters.ReservationFilter,
         template_name='staff_fuel_reservation_list.html'),
         name="staff_fuel_res_list"),
    path('staff/reservation/', views.FilteredReservationList.as_view(
        filterset_class=filters.ReservationFilter,
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
    path('staff/reservation/validation/<int:pk>/invalidate/',
         views.StaffReservationInvalidation.as_view(),
         name="staff_reservation_invalidate"),
]


# AJAX url
urlpatterns += [
    path('ajax/reservation/fuelserved/<int:pk>/', views.ajax_fuel_served,
         name="ajax_fuel_served"),
    path('ajax/add_ulm/<int:pk>/', views.ajax_add_ulm, name="ajax_add_ulm"),
    path('ajax/reservation/cancel/<int:pk>', views.ajax_cancel_reservation,
         name='ajax_cancel_reservation'),
    path('ajax/reservation/confirm/<int:pk>', views.ajax_confirm_reservation,
         name='ajax_confirm_reservation'),
]

# TODO: test to remove
urlpatterns += [
    path('test/email/base/', views.BaseEmailView.as_view(),
         name='base_email'),
    path('test/email/res_confirmation/',
         views.ReservationConfirmationEmail.as_view(),
         name='res_conf_email')
]
