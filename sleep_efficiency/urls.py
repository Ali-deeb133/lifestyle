from django.urls import path
from .views import (
    CreateSleepEntryView,
    LatestSleepEntryView,
    LatestSleepDetailsView
)

urlpatterns = [
    path("create/", CreateSleepEntryView.as_view()),
    path("latest/", LatestSleepEntryView.as_view()),
    path("latest/details/", LatestSleepDetailsView.as_view()),
]