from django.urls import path
from .views import BodyProfileCreateView, LatestBodyProfileView

urlpatterns = [
    path("create/", BodyProfileCreateView.as_view(), name="body-profile-create"),
    path("latest/", LatestBodyProfileView.as_view(), name="body-profile-latest"),
]