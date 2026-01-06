"""
AssetCategory Views - Dev A
Nhánh: feature/master-category
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from main.models import AssetCategory
from .serializers import AssetCategorySerializer


class AssetCategoryListView(generics.ListCreateAPIView):
    """GET/POST: Danh sách & tạo loại tài sản"""
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated]


class AssetCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE: Chi tiết loại tài sản"""
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated]
