from django.contrib import admin

from .models import Service, Appointment


# =========================================================
# SERVICE ADMIN
# =========================================================

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        "category",
        "name",
        "quality",
        "price",
        "duration",
        "active",
    )

    list_filter = (
        "category",
        "quality",
        "active",
    )

    search_fields = (
        "name",
        "category",
        "description",
    )

    list_editable = (
        "price",
        "duration",
        "active",
    )

    ordering = (
        "category",
        "price",
    )

    list_per_page = 20

    readonly_fields = ()

    fieldsets = (
        (
            "Service Information",
            {
                "fields": (
                    "category",
                    "name",
                    "quality",
                    "description",
                )
            }
        ),
        (
            "Pricing & Duration",
            {
                "fields": (
                    "price",
                    "duration",
                )
            }
        ),
        (
            "Service Image",
            {
                "fields": (
                    "image",
                )
            }
        ),
        (
            "Status",
            {
                "fields": (
                    "active",
                )
            }
        ),
    )


# =========================================================
# APPOINTMENT ADMIN
# =========================================================

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "service",
        "phone",
        "date",
        "time",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "date",
        "service__category",
        "service__quality",
    )

    search_fields = (
        "user__username",
        "phone",
        "service__name",
        "service__category",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-date",
        "-time",
    )

    list_per_page = 25

    date_hierarchy = "date"

    autocomplete_fields = (
        "user",
        "service",
    )