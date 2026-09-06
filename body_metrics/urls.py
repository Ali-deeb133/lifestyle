from django.urls import path
from .views import CalculateBodyMetricsView

urlpatterns = [
    path("calculate/", CalculateBodyMetricsView.as_view(),
         name="calculate-body-metrics"),
]