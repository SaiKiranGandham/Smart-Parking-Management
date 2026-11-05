

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from decimal import Decimal
from math import ceil

from .models import ParkingSlot, ParkingHistory, Reservation
from .forms import ReservationForm


# Dashboard
def dashboard(request):
    total_slots = ParkingSlot.objects.count()

    available_slots = ParkingSlot.objects.filter(
        status='available'
    ).count()

    occupied_slots = ParkingSlot.objects.filter(
        status='occupied'
    ).count()

    reserved_slots = ParkingSlot.objects.filter(
        status='reserved'
    ).count()

    slots = ParkingSlot.objects.all().order_by('slot_number')

    context = {
        'total_slots': total_slots,
        'available_slots': available_slots,
        'occupied_slots': occupied_slots,
        'reserved_slots': reserved_slots,
        'slots': slots,
    }

    return render(request, 'parking/dashboard.html', context)


# Update Parking Slot Status
@require_POST
def update_slot_status(request, slot_id):
    slot = get_object_or_404(ParkingSlot, id=slot_id)

    new_status = request.POST.get('status')

    if new_status in ['available', 'occupied', 'reserved']:
        slot.status = new_status
        slot.save()

    return redirect('dashboard')


# Vehicle Entry
@require_POST
def vehicle_entry(request, slot_id):
    slot = get_object_or_404(ParkingSlot, id=slot_id)

    vehicle_number = request.POST.get(
        'vehicle_number', ''
    ).strip().upper()

    if slot.status != 'available' or not vehicle_number:
        messages.error(request, 'Invalid vehicle entry.')
        return redirect('dashboard')

    active_vehicle = ParkingHistory.objects.filter(
        vehicle_number=vehicle_number,
        exit_time__isnull=True
    ).exists()

    if active_vehicle:
        messages.error(
            request,
            'This vehicle is already inside the parking facility.'
        )
        return redirect('dashboard')

    ParkingHistory.objects.create(
        vehicle_number=vehicle_number,
        slot=slot,
        entry_time=timezone.now()
    )

    slot.status = 'occupied'
    slot.save()

    messages.success(
        request,
        f'Vehicle {vehicle_number} entered successfully.'
    )

    return redirect('dashboard')


# Vehicle Exit and Automatic Billing
@require_POST
def vehicle_exit(request, slot_id):
    slot = get_object_or_404(ParkingSlot, id=slot_id)

    history = ParkingHistory.objects.filter(
        slot=slot,
        exit_time__isnull=True
    ).order_by('-entry_time').first()

    if history is None:
        messages.error(
            request,
            'No active vehicle found in this parking slot.'
        )
        return redirect('dashboard')

    exit_time = timezone.now()

    duration = (
        exit_time - history.entry_time
    ).total_seconds()

    hours = max(1, ceil(duration / 3600))
    fee = Decimal(hours * 20)

    history.exit_time = exit_time
    history.amount = fee
    history.save()

    slot.status = 'available'
    slot.save()

    messages.success(
        request,
        f'Vehicle {history.vehicle_number} exited successfully. '
        f'Parking Duration: {hours} hour(s). '
        f'Parking Fee: Rs. {fee:.2f}'
    )

    return redirect('dashboard')


# Create Reservation
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save()

            slot = reservation.slot
            slot.status = 'reserved'
            slot.save()

            messages.success(
                request,
                'Parking reservation created successfully!'
            )

            return redirect('dashboard')

    else:
        form = ReservationForm()

    return render(
        request,
        'parking/reservation_form.html',
        {'form': form}
    )


# Reservation List
def reservation_list(request):
    reservations = Reservation.objects.select_related(
        'slot'
    ).order_by('-created_at')

    return render(
        request,
        'parking/reservation_list.html',
        {'reservations': reservations}
    )


# Cancel Reservation
@require_POST
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id
    )

    slot = reservation.slot
    vehicle_number = reservation.vehicle_number

    reservation.delete()

    active_vehicle = ParkingHistory.objects.filter(
        slot=slot,
        exit_time__isnull=True
    ).exists()

    other_reservations = Reservation.objects.filter(
        slot=slot
    ).exists()

    if active_vehicle:
        slot.status = 'occupied'
    elif other_reservations:
        slot.status = 'reserved'
    else:
        slot.status = 'available'

    slot.save()

    messages.success(
        request,
        f'Reservation for {vehicle_number} cancelled successfully.'
    )

    return redirect('reservation_list')


# Parking History with Search and Filters
def parking_history(request):
    history_records = ParkingHistory.objects.select_related(
        'slot'
    ).order_by('-entry_time')

    search_query = request.GET.get('search', '').strip()

    if search_query:
        history_records = history_records.filter(
            vehicle_number__icontains=search_query
        )

    status = request.GET.get('status', '')

    if status == 'parked':
        history_records = history_records.filter(
            exit_time__isnull=True
        )

    elif status == 'completed':
        history_records = history_records.filter(
            exit_time__isnull=False
        )

    context = {
        'history_records': history_records,
        'search_query': search_query,
        'selected_status': status,
    }

    return render(
        request,
        'parking/parking_history.html',
        context
    )


# Parking Analytics
def parking_analytics(request):
    total_vehicles = ParkingHistory.objects.count()

    total_revenue = ParkingHistory.objects.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    currently_parked = ParkingHistory.objects.filter(
        exit_time__isnull=True
    ).count()

    completed_sessions = ParkingHistory.objects.filter(
        exit_time__isnull=False
    )

    completed_count = completed_sessions.count()

    average_fee = completed_sessions.aggregate(
        average=Sum('amount')
    )['average'] or Decimal('0.00')

    if completed_count:
        average_fee = average_fee / completed_count

    daily_revenue = ParkingHistory.objects.filter(
        exit_time__isnull=False
    ).annotate(
        day=TruncDate('exit_time')
    ).values(
        'day'
    ).annotate(
        revenue=Sum('amount'),
        vehicles=Count('id')
    ).order_by('-day')[:7]

    slot_usage = ParkingHistory.objects.values(
        'slot__slot_number'
    ).annotate(
        total_visits=Count('id')
    ).order_by('-total_visits')

    most_used_slot = slot_usage.first()

    context = {
        'total_vehicles': total_vehicles,
        'total_revenue': total_revenue,
        'currently_parked': currently_parked,
        'completed_count': completed_count,
        'average_fee': average_fee,
        'daily_revenue': daily_revenue,
        'most_used_slot': most_used_slot,
        'slot_usage': slot_usage,
    }

    return render(
        request,
        'parking/parking_analytics.html',
        context
    )
