
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path(
        'update-slot/<int:slot_id>/',
        views.update_slot_status,
        name='update_slot_status'
    ),

    path(
        'vehicle-entry/<int:slot_id>/',
        views.vehicle_entry,
        name='vehicle_entry'
    ),

    path(
        'vehicle-exit/<int:slot_id>/',
        views.vehicle_exit,
        name='vehicle_exit'
    ),

    path(
        'reservation/create/',
        views.create_reservation,
        name='create_reservation'
    ),

    path(
        'reservations/',
        views.reservation_list,
        name='reservation_list'
    ),

    path(
        'reservation/cancel/<int:reservation_id>/',
        views.cancel_reservation,
        name='cancel_reservation'
    ),

    path(
        'parking-history/',
        views.parking_history,
        name='parking_history'
    ),

    path(
        'parking-analytics/',
        views.parking_analytics,
        name='parking_analytics'
    ),
]
