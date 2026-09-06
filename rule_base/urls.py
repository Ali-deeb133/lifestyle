from django.urls import path
from .views import GenerateRuleBaseReportView

urlpatterns = [
    path("generate/", GenerateRuleBaseReportView.as_view(), name="generate-rule-report"),
]