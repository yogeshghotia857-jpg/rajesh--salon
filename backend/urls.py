from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from users import views


urlpatterns = [

    # =========================
    # HOME
    # =========================

    path(
        "",
        views.home,
        name="home"
    ),

    # =========================
    # ADMIN
    # =========================

    path(
        "admin/",
        admin.site.urls
    ),

    # =========================
    # AUTHENTICATION
    # =========================

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    # =========================
    # BOOKING
    # =========================

    path(
        "book/",
        views.book_appointment,
        name="book_appointment"
    ),

    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings"
    ),

    path(
        "cancel-booking/<int:appointment_id>/",
        views.cancel_booking,
        name="cancel_booking"
    ),
]


# =========================
# MEDIA FILES
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )