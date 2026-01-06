"""Location URLs - Dev A"""
from django.urls import path
from .views import LocationListView, LocationDetailView

app_name = 'location'

urlpatterns = [
    path('', LocationListView.as_view(), name='location-list'),
    path('<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
]
