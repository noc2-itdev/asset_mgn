"""
AuditAction URLs
================

Người phụ trách: [Dev C3]

Base paths:
- /api/audit-items/<item_id>/actions/
- /api/audit-actions/
"""

from django.urls import path
from ..views import (
    AuditActionListView,
    AuditActionDetailView,
    approve_action,
    reject_action,
    execute_action,
)

urlpatterns = [
    # Actions của item
    path('audit-items/<int:item_id>/actions/', AuditActionListView.as_view(), name='action-list'),
    
    # Action detail & workflow
    path('audit-actions/<int:pk>/', AuditActionDetailView.as_view(), name='action-detail'),
    path('audit-actions/<int:pk>/approve/', approve_action, name='action-approve'),
    path('audit-actions/<int:pk>/reject/', reject_action, name='action-reject'),
    path('audit-actions/<int:pk>/execute/', execute_action, name='action-execute'),
]
