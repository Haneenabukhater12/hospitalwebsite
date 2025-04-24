# surgery/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('surgeon', 'Surgeon'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class OperationRoom(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"OR {self.room_number}"

class SurgeryCase(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='surgery_cases'
    )
    surgeon = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='surgeries'
    )
    operation_room = models.ForeignKey(
        OperationRoom,
        on_delete=models.PROTECT
    )
    date_time = models.DateTimeField()
    procedure_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.procedure_type} on {self.date_time.date()}"


class PreOpChecklist(models.Model):
    surgery_case = models.OneToOneField(SurgeryCase, on_delete=models.CASCADE)
    consent_signed = models.BooleanField(default=False)
    allergies_checked = models.BooleanField(default=False)
    lab_results_approved = models.BooleanField(default=False)


class PostOpReport(models.Model):
    surgery_case = models.OneToOneField(SurgeryCase, on_delete=models.CASCADE)
    outcome = models.TextField()  # it describes the operation outcome (succeeded/failed)
    notes = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)



