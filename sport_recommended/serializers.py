from rest_framework import serializers
from .models import Level, Goal

class RecommendationInputSerializer(serializers.Serializer):
    level = serializers.CharField()
    goal = serializers.CharField()
    equipment = serializers.CharField()
    program_length = serializers.IntegerField(min_value=1, max_value=18)

    def validate(self, data):
        if not Level.objects.filter(name=data["level"]).exists():
            raise serializers.ValidationError({"level": f"Invalid level"})
        if not Goal.objects.filter(name=data["goal"]).exists():
            raise serializers.ValidationError({"goal": f"Invalid goal"})
        return data