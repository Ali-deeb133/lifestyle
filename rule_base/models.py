from django.db import models
from django.conf import settings
from django.utils import timezone
from body_metrics.models import BodyMetrics

class RuleBaseReport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rule_base_reports"
    )
    body_metrics = models.ForeignKey(
        BodyMetrics,
        on_delete=models.CASCADE
    )

    # التصنيفات لكل بارامتر
    bmi_category = models.CharField(max_length=50)
    bfp_category = models.CharField(max_length=50)
    lean_mass_category = models.CharField(max_length=50)
    fat_mass_category = models.CharField(max_length=50)
    bmr_category = models.CharField(max_length=50)
    tdee_category = models.CharField(max_length=50)
    fat_to_lose_status = models.CharField(max_length=50)
    ideal_bfp_deviation = models.CharField(max_length=50)

    # الطبقة النهائية
    primary_pattern = models.CharField(max_length=100)
    segment = models.CharField(max_length=50)
    metabolic_status = models.CharField(max_length=50)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.primary_pattern} - {self.created_at.date()}"