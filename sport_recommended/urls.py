from django.urls import path
from .views import RecommendProgramAPIView

urlpatterns = [
    path("recommend/", RecommendProgramAPIView.as_view(), name="recommend-program"),
]