"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/body_profiles/', include('body_profiles.urls')),
    path("api/body-metrics/", include("body_metrics.urls")),
    path("api/rule-base/", include("rule_base.urls")),
    path("api/sleep/", include("sleep_efficiency.urls")),
    # path("api/sport/", include("sports_recommendation.urls")),
    path('api/sport/', include('sport_recommended.urls')),
]
