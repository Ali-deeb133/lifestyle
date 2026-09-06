from django.contrib import admin
from .models import SleepEntry


@admin.register(SleepEntry)
class SleepEntryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "predicted_efficiency",
        "efficiency_label",
        "sleep_duration",
        "caffeine_mg",
        "alcohol_grams",
        "created_at"
    )

    list_filter = (
        "efficiency_label",
        "smoking_status",
        "gender",
        "created_at"
    )

    search_fields = ("user__email",)
    ordering = ("-created_at",)