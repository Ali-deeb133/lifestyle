from django.db import models
from django.conf import settings
from django.utils import timezone


class BodyMetrics(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="body_metrics"
    )

    body_profile = models.ForeignKey(
        "body_profiles.BodyProfile",
        on_delete=models.CASCADE
    )

    age = models.IntegerField()
    activity_factor = models.FloatField()

    bmi = models.FloatField()
    body_fat_percentage = models.FloatField()

    fat_mass = models.FloatField()
    lean_mass = models.FloatField()

    ideal_body_fat_percentage = models.FloatField()
    fat_to_lose = models.FloatField()

    bmr = models.FloatField()
    tdee = models.FloatField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - Metrics - {self.created_at.date()}"