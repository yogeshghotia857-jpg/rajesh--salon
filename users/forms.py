from django import forms
from django.utils import timezone
from datetime import datetime, timedelta
import re

from .models import Appointment, Service


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = [
            "service",
            "date",
            "time",
            "phone",
        ]

        widgets = {
            "service": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter phone number",
                    "maxlength": "15",
                    "autocomplete": "tel",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only active services should be available for booking
        self.fields["service"].queryset = (
            Service.objects
            .filter(active=True)
            .order_by("category", "price")
        )

        self.fields["service"].label = "Select Service"
        self.fields["date"].label = "Appointment Date"
        self.fields["time"].label = "Appointment Time"
        self.fields["phone"].label = "Phone Number"

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        # Keep only digits for validation
        digits = re.sub(r"\D", "", phone)

        if not digits:
            raise forms.ValidationError(
                "Please enter your phone number."
            )

        if len(digits) < 10 or len(digits) > 15:
            raise forms.ValidationError(
                "Please enter a valid phone number."
            )

        return phone

    def clean_date(self):
        date = self.cleaned_data.get("date")

        if not date:
            return date

        today = timezone.localdate()

        if date < today:
            raise forms.ValidationError(
                "You cannot book an appointment for a past date."
            )

        return date

    def clean(self):
        cleaned_data = super().clean()

        service = cleaned_data.get("service")
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if not service or not date or not time:
            return cleaned_data

        # -----------------------------------------
        # Prevent booking a past time today
        # -----------------------------------------

        today = timezone.localdate()
        current_time = timezone.localtime().time()

        if date == today and time < current_time:
            self.add_error(
                "time",
                "Please select a future time."
            )

            return cleaned_data

        # -----------------------------------------
        # New appointment time range
        # -----------------------------------------

        new_start = datetime.combine(
            date,
            time
        )

        new_end = (
            new_start
            + timedelta(
                minutes=service.duration
            )
        )

        # -----------------------------------------
        # Existing appointments
        # -----------------------------------------

        appointments = (
            Appointment.objects
            .filter(date=date)
            .exclude(pk=self.instance.pk)
            .select_related("service")
        )

        for appointment in appointments:

            # Cancelled bookings do not occupy a slot
            if appointment.status == "Cancelled":
                continue

            old_start = datetime.combine(
                appointment.date,
                appointment.time
            )

            old_end = (
                old_start
                + timedelta(
                    minutes=appointment.service.duration
                )
            )

            # Check whether two appointments overlap
            if (
                new_start < old_end
                and
                new_end > old_start
            ):
                raise forms.ValidationError(
                    "This time slot is not available "
                    "because it overlaps with another "
                    "appointment. Please select another time."
                )

        return cleaned_data