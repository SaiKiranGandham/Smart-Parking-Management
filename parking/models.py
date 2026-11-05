from django.db import models


class ParkingSlot(models.Model):
    SLOT_STATUS = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
    ]

    slot_number = models.CharField(max_length=20, unique=True)
    floor = models.IntegerField(default=1)
    vehicle_type = models.CharField(max_length=20, default='Car')
    status = models.CharField(
        max_length=20,
        choices=SLOT_STATUS,
        default='available'
    )

    def __str__(self):
        return self.slot_number


class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vehicle_number


class ParkingHistory(models.Model):
    vehicle_number = models.CharField(max_length=20)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.vehicle_number