from rest_framework import serializers
from .models import SleepEntry
from body_metrics.models import BodyMetrics
from body_profiles.models import BodyProfile


class SleepEntrySerializer(serializers.ModelSerializer):

    coffee_cups = serializers.IntegerField(write_only=True)
    alcohol_glasses = serializers.IntegerField(write_only=True)

    class Meta:
        model = SleepEntry
        fields = "__all__"
        read_only_fields = (
            "user",
            "age",
            "gender",
            "caffeine_mg",
            "alcohol_grams",
            "predicted_efficiency",
            "efficiency_label",
            "created_at",
        )

    def validate_sleep_duration(self, value):
        if value < 1 or value > 24:
            raise serializers.ValidationError("Sleep duration must be between 1 and 24.")
        return value

    def validate_exercise_frequency(self, value):
        if value < 0 or value > 7:
            raise serializers.ValidationError("Exercise frequency must be between 0 and 7.")
        return value

    def validate_awakenings(self, value):
        if value < 0:
            raise serializers.ValidationError("Awakenings cannot be negative.")
        return value

    # def create(self, validated_data):
    #     coffee_cups = validated_data.pop("coffee_cups")
    #     alcohol_glasses = validated_data.pop("alcohol_glasses")

    #     validated_data["caffeine_mg"] = coffee_cups * 80
    #     validated_data["alcohol_grams"] = alcohol_glasses * 14

    #     validated_data["user"] = self.context["request"].user

    #     return super().create(validated_data)
    
    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        # 🔹 جلب أحدث BodyMetrics
        metrics = BodyMetrics.objects.filter(
            user=user
        ).order_by("-created_at").first()

        if not metrics:
            raise serializers.ValidationError(
                "You must calculate body metrics first."
            )

        # 🔹 جلب BodyProfile
        profile = BodyProfile.objects.filter(
            user=user
        ).order_by("-created_at").first()

        if not profile:
            raise serializers.ValidationError(
                "Body profile not found."
            )

        # تحويل القهوة والكحول
        coffee_cups = validated_data.pop("coffee_cups")
        alcohol_glasses = validated_data.pop("alcohol_glasses")

        validated_data["caffeine_mg"] = coffee_cups * 80
        validated_data["alcohol_grams"] = alcohol_glasses * 14

 
        validated_data["age"] = metrics.age
        validated_data["gender"] = profile.gender
        validated_data["user"] = user

        return super().create(validated_data)