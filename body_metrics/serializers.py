import math
from datetime import date
from rest_framework import serializers
from .models import BodyMetrics
from body_profiles.models import BodyProfile


class BodyMetricsSerializer(serializers.ModelSerializer):

    warnings = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BodyMetrics
        exclude = ("user", "body_profile")
        read_only_fields = (
            "age",
            "activity_factor",
            "bmi",
            "body_fat_percentage",
            "fat_mass",
            "lean_mass",
            "ideal_body_fat_percentage",
            "fat_to_lose",
            "bmr",
            "tdee",
            "created_at",
        )

    def create(self, validated_data):

        user = self.context["request"].user

        profile = BodyProfile.objects.filter(
            user=user
        ).order_by("-created_at").first()

        if not profile:
            raise serializers.ValidationError(
                "No measurements. Please enter your body data first."
            )

        warnings = []

        # ---------------- AGE ----------------
        today = date.today()
        age = today.year - profile.birth_date.year - (
            (today.month, today.day) <
            (profile.birth_date.month, profile.birth_date.day)
        )

        # ---------------- ACTIVITY FACTOR ----------------
        activity_map = {
            "very_low": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "high": 1.725,
            "very_high": 1.9,
            "none": 1.2,
        }

        activity_factor = activity_map.get(profile.activity_level, 1.2)

        # ---------------- BMI ----------------
        height_m = profile.height / 100
        bmi = profile.weight / (height_m ** 2)

        if bmi < 10 or bmi > 70:
            raise serializers.ValidationError(
                {"bmi": "The BMI value is illogical. Please adjust your body measurements."}
            )

        if bmi < 14 or bmi > 45:
            warnings.append("BMI value unusual.")

        # ---------------- BFP ----------------
        if profile.gender == "male":
            bfp = (
                495 /
                (1.0324 - 0.19077 *
                 math.log10(profile.waist_circumference - profile.neck_circumference)
                 + 0.15456 * math.log10(profile.height))
            ) - 450
        else:
            bfp = (
                495 /
                (1.29579 - 0.35004 *
                 math.log10(profile.waist_circumference +
                            profile.hip_circumference -
                            profile.neck_circumference)
                 + 0.22100 * math.log10(profile.height))
            ) - 450

        # HARD BFP
        if (profile.gender == "male" and bfp < 3) or \
           (profile.gender == "female" and bfp < 5) or \
           bfp > 60:
            raise serializers.ValidationError(
                {"body_fat_percentage":
                 "The body fat percentage is illogical. Please adjust your body measurements."}
            )

        # WARNING BFP
        if (profile.gender == "male" and (bfp < 6 or bfp > 35)) or \
           (profile.gender == "female" and (bfp < 12 or bfp > 45)):
            warnings.append("Body fat percentage unusual.")

        # ---------------- FAT MASS ----------------
        fat_mass = profile.weight * (bfp / 100)

        if fat_mass > profile.weight:
            raise serializers.ValidationError(
                {"fat_mass": "The value for fat mass is illogical."}
            )

        # ---------------- LEAN MASS ----------------
        lean_mass = profile.weight - fat_mass

        if lean_mass <= 0:
            raise serializers.ValidationError(
                {"lean_mass": "The value of lean body mass is illogical."}
            )

        if lean_mass < profile.weight * 0.4:
            warnings.append("Lean mass unusually low.")

        # ---------------- IDEAL FAT ----------------
        ideal_table = {
            20: {"male": 8.5, "female": 17.7},
            25: {"male": 10.5, "female": 18.4},
            30: {"male": 12.7, "female": 19.3},
            35: {"male": 13.7, "female": 21.5},
            40: {"male": 15.3, "female": 22.2},
            45: {"male": 16.4, "female": 22.9},
            50: {"male": 18.9, "female": 25.2},
            55: {"male": 20.9, "female": 26.3},
        }

        closest_age = min(ideal_table.keys(),
                          key=lambda x: abs(x - age))

        if age > 55:
            ideal_bfp = ideal_table[55][profile.gender]
        else:
            ideal_bfp = ideal_table[closest_age][profile.gender]

        ideal_fm = profile.weight * (ideal_bfp / 100)
        fat_to_lose = fat_mass - ideal_fm

        # ---------------- BMR ----------------
        if profile.gender == "male":
            bmr = 10 * profile.weight + 6.25 * \
                profile.height - 5 * age + 5
        else:
            bmr = 10 * profile.weight + 6.25 * \
                profile.height - 5 * age - 161

        # ---------------- TDEE ----------------
        tdee = bmr * activity_factor

        self._warnings = warnings

        return BodyMetrics.objects.create(
            user=user,
            body_profile=profile,
            age=age,
            activity_factor=activity_factor,
            bmi=round(bmi, 2),
            body_fat_percentage=round(bfp, 2),
            fat_mass=round(fat_mass, 2),
            lean_mass=round(lean_mass, 2),
            ideal_body_fat_percentage=ideal_bfp,
            fat_to_lose=round(fat_to_lose, 2),
            bmr=round(bmr, 2),
            tdee=round(tdee, 2),
        )

    def get_warnings(self, obj):
        return getattr(self, "_warnings", [])