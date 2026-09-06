from rest_framework import serializers
from .models import RuleBaseReport

class RuleBaseReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleBaseReport
        fields = "__all__"
        read_only_fields = [
            "user",
            "body_metrics",
            "bmi_category",
            "bfp_category",
            "lean_mass_category",
            "fat_mass_category",
            "bmr_category",
            "tdee_category",
            "fat_to_lose_status",
            "ideal_bfp_deviation",
            "primary_pattern",
            "segment",
            "metabolic_status",
            "created_at",
        ]