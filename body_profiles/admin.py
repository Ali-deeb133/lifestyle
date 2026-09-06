from django.contrib import admin
from .models import BodyProfile


@admin.register(BodyProfile)
class BodyProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "gender",
        "height",
        "weight",
        "activity_level",
        "created_at",
    )

    list_filter = (
        "gender",
        "activity_level",
        "created_at",
    )

    search_fields = (
        "user__email",
    )

    ordering = ("-created_at",)