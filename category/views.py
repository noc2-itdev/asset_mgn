"""
AssetCategory Views - CRUD Loại tài sản
=======================================

Người phụ trách: [Dev A]
Nhánh Git: feature/master-category
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from main.models import AssetCategory
from .serializers import AssetCategorySerializer


class AssetCategoryListView(generics.ListCreateAPIView):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated]


class AssetCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated]
