"""Department URLs - Dev A"""
from django.urls import path
from .views import DepartmentListView, DepartmentDetailView

app_name = 'department'

urlpatterns = [
    path('', DepartmentListView.as_view(), name='department-list'),
    path('<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
]
