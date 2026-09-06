from rest_framework import serializers
from datetime import date
from .models import BodyProfile


class BodyProfileSerializer(serializers.ModelSerializer):

    warnings = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BodyProfile
        exclude = ("user",)

    # -------------------------
    # AGE CALCULATION
    # -------------------------
    def validate_birth_date(self, value):
        today = date.today()
        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )

        if age < 20 or age > 80:
            raise serializers.ValidationError(
                "We apologize, this site is not suitable for this age group."
            )
        return value

    # -------------------------
    # MAIN VALIDATION
    # -------------------------
    def validate(self, data):

        warnings = []

        height = data.get("height")
        weight = data.get("weight")
        gender = data.get("gender")
        neck = data.get("neck_circumference")
        waist = data.get("waist_circumference")
        hip = data.get("hip_circumference")

        # ---------------- HARD ERRORS ----------------

        if height < 100 or height > 250:
            raise serializers.ValidationError({"height": "Invalid height value."})

        if weight < 20 or weight > 350:
            raise serializers.ValidationError({"weight": "Invalid weight value."})

        if neck < 20 or neck > 70:
            raise serializers.ValidationError({"neck_circumference": "Invalid neck value."})

        if waist < 40 or waist > 200:
            raise serializers.ValidationError({"waist_circumference": "Invalid waist value."})

        if gender == "male" and hip:
            raise serializers.ValidationError({"hip_circumference": "Hip not allowed for males."})

        if gender == "female":
            if not hip:
                raise serializers.ValidationError({"hip_circumference": "Required for females."})
            if hip < 50 or hip > 200:
                raise serializers.ValidationError({"hip_circumference": "Invalid hip value."})

        if neck >= waist:
            raise serializers.ValidationError("Neck must be smaller than waist.")

        if abs(waist - neck) < 3:
            raise serializers.ValidationError("The difference between the neck and waist should be at least 3 cm.")

        # ---------------- WARNINGS ----------------

        if weight < 40 or weight > 200:
            warnings.append("Weight value is unusual.")

        if gender == "male" and (height < 145 or height > 210):
            warnings.append("Height unusual for male.")

        if gender == "female" and (height < 140 or height > 200):
            warnings.append("Height unusual for female.")

        if gender == "male" and (neck < 32 or neck > 55):
            warnings.append("Neck unusual for male.")

        if gender == "female" and (neck < 27 or neck > 45):
            warnings.append("Neck unusual for female.")

        if gender == "male" and (waist < 65 or waist > 150):
            warnings.append("Waist unusual for male.")

        if gender == "female" and (waist < 60 or waist > 140):
            warnings.append("Waist unusual for female.")

        if gender == "female" and hip:
            if hip < 75 or hip > 160:
                warnings.append("Hip unusual value.")

        self._warnings = warnings
        return data

    def get_warnings(self, obj):
        return getattr(self, "_warnings", [])