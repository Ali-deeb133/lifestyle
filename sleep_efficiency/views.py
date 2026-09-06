from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import SleepEntry
from .serializers import SleepEntrySerializer
from .ml_model import rf_model, preprocessor
from rest_framework.views import APIView
import pandas as pd

class CreateSleepEntryView(generics.CreateAPIView):
    serializer_class = SleepEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()

        X_user = pd.DataFrame([{
            'Age': instance.age,
            'Sleep duration': instance.sleep_duration,
            'Exercise frequency': instance.exercise_frequency,
            'Smoking status': 'Yes' if instance.smoking_status else 'No',
            'Gender': instance.gender,
            'Bedtime': f"2021-01-01 {instance.bed_time}",
            'Caffeine consumption': instance.caffeine_mg,
            'Alcohol consumption': instance.alcohol_grams,
            'Awakenings': instance.awakenings
        }])

        X_processed = preprocessor.transform(X_user)
        efficiency = rf_model.predict(X_processed)[0]

        percent = round(efficiency * 100)

        if percent >= 75:
            label = "Good sleep efficiency"
        elif percent >= 50:
            label = "Moderate sleep efficiency"
        else:
            label = "Poor sleep efficiency"

        instance.predicted_efficiency = percent
        instance.efficiency_label = label
        instance.save()


class LatestSleepEntryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        entry = SleepEntry.objects.filter(
            user=request.user
        ).order_by("-created_at").first()

        if not entry:
            return Response(
                {"detail": "No sleep records found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "predicted_efficiency": entry.predicted_efficiency,
            "efficiency_label": entry.efficiency_label,
            "created_at": entry.created_at
        })

class LatestSleepDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        entry = SleepEntry.objects.filter(
            user=request.user
        ).order_by("-created_at").first()

        if not entry:
            return Response(
                {"detail": "No sleep records found."},
                status=status.HTTP_404_NOT_FOUND
            )

        def analyze_sleep_duration(hours):
            if hours < 4:
                return "Severe deprivation"
            elif 7 <= hours <= 9:
                return "Ideal"
            elif hours > 10:
                return "Too long"
            return "Moderate"

        return Response({
            "sleep_efficiency": entry.predicted_efficiency,
            "classification": entry.efficiency_label,
            "factors_analysis": {
                "sleep_duration": {
                    "value": entry.sleep_duration,
                    "evaluation": analyze_sleep_duration(entry.sleep_duration)
                },
                "caffeine": {
                    "value": entry.caffeine_mg,
                    "evaluation": "High" if entry.caffeine_mg > 200 else "Normal"
                },
                "alcohol": {
                    "value": entry.alcohol_grams,
                    "evaluation": "High" if entry.alcohol_grams > 20 else "Normal"
                },
                "awakenings": {
                    "value": entry.awakenings,
                    "evaluation": "Frequent" if entry.awakenings > 3 else "Light"
                },
                "exercise_frequency": {
                    "value": entry.exercise_frequency,
                    "evaluation": "Good" if entry.exercise_frequency >= 3 else "Low"
                }
            }
        })