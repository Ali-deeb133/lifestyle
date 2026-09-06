from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone


class BodyProfile(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("none", "Not Specified"),
    )

    ACTIVITY_LEVEL_CHOICES = (
        ("none", "None"),
        ("very_low", "Very Low"),
        ("light", "Light"),
        ("moderate", "Moderate"),
        ("high", "High"),
        ("very_high", "Very High"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="body_profile"
    )

    birth_date = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default="none"
    )

    height = models.FloatField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])

    neck_circumference = models.FloatField(validators=[MinValueValidator(0)])
    waist_circumference = models.FloatField(validators=[MinValueValidator(0)])
    hip_circumference = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    activity_level = models.CharField(
        max_length=20,
        choices=ACTIVITY_LEVEL_CHOICES,
        default="none"
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - Body Profile"