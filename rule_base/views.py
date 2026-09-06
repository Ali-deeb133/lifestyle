from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import RuleBaseReport
from .serializers import RuleBaseReportSerializer
from body_metrics.models import BodyMetrics
from .utils.rule_engine import *

class GenerateRuleBaseReportView(generics.CreateAPIView):
    serializer_class = RuleBaseReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # أخذ أحدث BodyMetrics
        metrics = BodyMetrics.objects.filter(
            user=request.user
        ).order_by("-created_at").first()

        if not metrics:
            return Response(
                {"detail": "No body metrics found. Please calculate metrics first."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # حساب التصنيفات
        bmi_cat, bmi_meaning = classify_bmi(metrics.bmi)
        bfp_cat, bfp_meaning = classify_bfp(metrics.body_fat_percentage, metrics.body_profile.gender)
        lean_cat, lean_meaning = classify_lean_mass(metrics.lean_mass / metrics.body_profile.weight * 100)
        fat_cat, fat_meaning = classify_fat_mass(metrics.fat_mass / metrics.body_profile.weight * 100)
        bmr_cat, bmr_meaning = classify_bmr(metrics.bmr, metrics.body_profile.gender)
        tdee_cat, tdee_meaning = classify_tdee(metrics.tdee)

        # Fat to lose
        if metrics.fat_to_lose > 0:
            fat_to_lose_status = "Must Reduce"
        else:
            fat_to_lose_status = "No Fat Loss Needed"

        # Ideal deviation
        diff = abs(metrics.body_fat_percentage - metrics.ideal_body_fat_percentage)
        if diff <= 2:
            ideal_dev = "Excellent alignment"
        elif diff <= 5:
            ideal_dev = "Slight deviation"
        elif diff <= 10:
            ideal_dev = "Moderate imbalance"
        else:
            ideal_dev = "Significant imbalance"

        # Decision Matrix Layer
        # هنا نحدد primary_pattern, segment, metabolic_status
        # Simplified example (يمكن تطويره مع كل branch والأولويات)
        segment = "Normal"
        if metrics.bmi < 18.5: segment = "Underweight"
        elif metrics.bmi >= 25: segment = "Overweight"
        if metrics.bmi >= 35: segment = "Obese"

        # primary_pattern - حسب الأولوية
        primary_pattern = "Balanced Body Composition"
        if lean_cat == "Very Low" and bmr_cat in ["Low", "Very Low"]:
            primary_pattern = "Severe Muscle Deficiency"
        elif bfp_cat in ["Obese", "Very High"] and lean_cat == "Low":
            primary_pattern = "Sarcopenic Obesity"
        elif bfp_cat in ["Healthy", "Overfat", "Obese"] and lean_cat in ["Low", "Very Low"]:
            primary_pattern = "Skinny Fat"
        elif bmr_cat in ["Low", "Very Low"] and tdee_cat in ["Low", "Moderate"]:
            primary_pattern = "Metabolic Suppression"

        # metabolic_status
        metabolic_status = "Normal"
        if bmr_cat in ["Very Low", "Low"] and tdee_cat in ["Low", "Moderate"]:
            metabolic_status = "Suppressed"
        elif bmr_cat == "Average" and tdee_cat == "Moderate":
            metabolic_status = "Normal"
        elif bmr_cat == "High" and tdee_cat == "Active":
            metabolic_status = "Elevated"
        elif bmr_cat in ["Very High"] and tdee_cat == "Highly Active":
            metabolic_status = "Hypermetabolic"

        # حفظ التقرير
        report = RuleBaseReport.objects.create(
            user=request.user,
            body_metrics=metrics,
            bmi_category=bmi_cat,
            bfp_category=bfp_cat,
            lean_mass_category=lean_cat,
            fat_mass_category=fat_cat,
            bmr_category=bmr_cat,
            tdee_category=tdee_cat,
            fat_to_lose_status=fat_to_lose_status,
            ideal_bfp_deviation=ideal_dev,
            primary_pattern=primary_pattern,
            segment=segment,
            metabolic_status=metabolic_status
        )

        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)