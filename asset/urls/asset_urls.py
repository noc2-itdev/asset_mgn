"""Asset CRUD URLs - Dev B1"""
from django.urls import path
from ..views import AssetListView, AssetDetailView, qr_lookup, AssetHistoryListView

urlpatterns = [
    path('', AssetListView.as_view(), name='asset-list'),
    path('<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),
    path('qr/<str:code>/', qr_lookup, name='asset-qr-lookup'),
    path('<int:pk>/history/', AssetHistoryListView.as_view(), name='asset-history'),
]
