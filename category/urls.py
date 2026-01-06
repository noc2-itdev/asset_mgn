"""Category URLs - Dev A"""
from django.urls import path
from .views import AssetCategoryListView, AssetCategoryDetailView

app_name = 'category'

urlpatterns = [
    path('', AssetCategoryListView.as_view(), name='list'),
    path('<int:pk>/', AssetCategoryDetailView.as_view(), name='detail'),
]
