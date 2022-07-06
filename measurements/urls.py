from django.urls import path
from .views import calculateDistanceView

app_name = 'measurements'

urlpatterns = [
    path('', calculateDistanceView, name = 'calculateDistanceView')
]