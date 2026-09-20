from django.contrib.auth.models import User
from django.db import models


class Service(models.Model):

    CATEGORY_CHOICES = [
        ("Haircut", "Haircut"),
        ("Beard", "Beard"),
        ("Hair Color", "Hair Color"),
        ("Facial", "Facial"),
        ("Hair Styling", "Hair Styling"),
        ("Hair Spa", "Hair Spa"),
        ("Other", "Other"),
    ]

    QUALITY_CHOICES = [
        ("Basic", "Basic"),
        ("Premium", "Premium"),
        ("Luxury", "Luxury"),
    ]

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    name = models.CharField(
        max_length=100
    )

    quality = models.CharField(
        max_length=50,
        choices=QUALITY_CHOICES,
        default="Basic"
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in minutes"
    )

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.category} - {self.name} ({self.quality})"


class Appointment(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    time = models.TimeField()

    phone = models.CharField(
        max_length=15
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.service} - "
            f"{self.date}"
        )