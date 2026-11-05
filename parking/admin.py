from django.contrib import admin
from .models import ParkingSlot, Reservation, ParkingHistory


@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'floor', 'vehicle_type', 'status')
    list_filter = ('status', 'floor', 'vehicle_type')
    search_fields = ('slot_number',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'vehicle_number',
        'slot',
        'start_time',
        'end_time'
    )
    search_fields = ('customer_name', 'vehicle_number')


@admin.register(ParkingHistory)
class ParkingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle_number',
        'slot',
        'entry_time',
        'exit_time',
        'amount'
    )
    search_fields = ('vehicle_number',)