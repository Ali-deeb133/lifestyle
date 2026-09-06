from django.contrib import admin
from .models import BodyMetrics


@admin.register(BodyMetrics)
class BodyMetricsAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "bmi",
        "body_fat_percentage",
        "bmr",
        "tdee",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = ("user__email",)
    ordering = ("-created_at",)