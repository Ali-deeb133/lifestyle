from django.contrib import admin
from .models import RuleBaseReport

@admin.register(RuleBaseReport)
class RuleBaseReportAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "primary_pattern",
        "segment",
        "metabolic_status",
        "created_at"
    )
    list_filter = ("segment", "primary_pattern", "metabolic_status", "created_at")
    search_fields = ("user__email",)
    ordering = ("-created_at",)