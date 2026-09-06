from django.db import models
from django.conf import settings
from django.utils import timezone


class SleepEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sleep_entries"
    )

    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    sleep_duration = models.FloatField()
    exercise_frequency = models.IntegerField()
    smoking_status = models.BooleanField()

    bed_time = models.TimeField()

    caffeine_mg = models.FloatField()
    alcohol_grams = models.FloatField()

    awakenings = models.IntegerField()

    predicted_efficiency = models.IntegerField(null=True, blank=True)
    efficiency_label = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.predicted_efficiency}%"