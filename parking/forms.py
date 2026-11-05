from django import forms
from django.utils import timezone
from .models import Reservation, ParkingHistory


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation

        fields = [
            'customer_name',
            'vehicle_number',
            'slot',
            'start_time',
            'end_time',
        ]

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name'
            }),

            'vehicle_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter vehicle number'
            }),

            'slot': forms.Select(attrs={
                'class': 'form-control'
            }),

            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),

            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        slot = cleaned_data.get('slot')

        if start_time and end_time:

            if end_time <= start_time:
                raise forms.ValidationError(
                    'End time must be after start time.'
                )

            if start_time < timezone.now():
                raise forms.ValidationError(
                    'Reservation start time must be in the future.'
                )

        if slot:

            if slot.status == 'occupied':
                raise forms.ValidationError(
                    'This parking slot is currently occupied.'
                )

            active_vehicle = ParkingHistory.objects.filter(
                slot=slot,
                exit_time__isnull=True
            ).exists()

            if active_vehicle:
                raise forms.ValidationError(
                    'A vehicle is currently parked in this slot.'
                )

            if start_time and end_time:

                overlapping = Reservation.objects.filter(
                    slot=slot,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exclude(
                    pk=self.instance.pk
                ).exists()

                if overlapping:
                    raise forms.ValidationError(
                        'This slot is already reserved during the selected time.'
                    )

        return cleaned_data