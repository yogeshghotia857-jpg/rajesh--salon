from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Appointment, Service
from .forms import AppointmentForm


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            messages.success(
                request,
                "Account created successfully!"
            )

            return redirect("/")

    else:
        form = UserCreationForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("/")

        return render(
            request,
            "login.html",
            {
                "error":
                    "Invalid username or password."
            }
        )

    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect(
        "/login/"
    )


# =========================================================
# HOME
# =========================================================

def home(request):

    services = (
        Service.objects
        .filter(
            active=True
        )
        .order_by(
            "category",
            "price"
        )
    )

    return render(
        request,
        "home.html",
        {
            "services": services
        }
    )


# =========================================================
# BOOK APPOINTMENT
# =========================================================

@login_required(login_url="/login/")
def book_appointment(request):

    service_id = request.GET.get(
        "service"
    )

    if request.method == "POST":

        form = AppointmentForm(
            request.POST
        )

        if form.is_valid():

            appointment = form.save(
                commit=False
            )

            appointment.user = (
                request.user
            )

            appointment.save()

            messages.success(
                request,
                "Your appointment has been booked successfully!"
            )

            return render(
                request,
                "booking_success.html",
                {
                    "appointment":
                        appointment
                }
            )

    else:

        form = AppointmentForm()

        # Pre-select service when
        # user clicks Book Now
        if service_id:

            try:

                service_id = int(
                    service_id
                )

                service_exists = (
                    Service.objects
                    .filter(
                        id=service_id,
                        active=True
                    )
                    .exists()
                )

                if service_exists:

                    form.fields[
                        "service"
                    ].initial = service_id

            except (
                ValueError,
                TypeError
            ):
                pass

    return render(
        request,
        "booking.html",
        {
            "form": form
        }
    )


# =========================================================
# MY BOOKINGS
# =========================================================

@login_required(login_url="/login/")
def my_bookings(request):

    appointments = (
        Appointment.objects
        .filter(
            user=request.user
        )
        .select_related(
            "service"
        )
        .order_by(
            "-date",
            "-time"
        )
    )

    return render(
        request,
        "my_bookings.html",
        {
            "appointments":
                appointments
        }
    )


# =========================================================
# CANCEL BOOKING
# =========================================================

@login_required(login_url="/login/")
def cancel_booking(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        user=request.user
    )

    if request.method == "POST":

        if appointment.status != "Cancelled":

            appointment.status = "Cancelled"

            appointment.save(
                update_fields=[
                    "status"
                ]
            )

            messages.success(
                request,
                "Your appointment has been cancelled."
            )

        else:

            messages.info(
                request,
                "This appointment is already cancelled."
            )

    return redirect(
        "/my-bookings/"
    )