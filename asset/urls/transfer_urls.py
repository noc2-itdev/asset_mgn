"""Transfer URLs - Dev B3"""
from django.urls import path
from ..views import transfer_asset, AssetAttachmentListView

urlpatterns = [
    path('<int:pk>/transfer/', transfer_asset, name='asset-transfer'),
    path('<int:pk>/attachments/', AssetAttachmentListView.as_view(), name='asset-attachments'),
]
