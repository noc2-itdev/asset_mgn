"""
AuditItem URLs
==============

Người phụ trách: [Dev C2]

Base paths:
- /api/audit-sessions/<session_id>/items/
- /api/audit-items/
"""

from django.urls import path
from ..views import (
    AuditItemListView,
    AuditItemDetailView,
    add_items_manual,
    remove_items,
    check_item,
    mark_missing,
)

urlpatterns = [
    # Items trong session
    path('audit-sessions/<int:session_id>/items/', AuditItemListView.as_view(), name='item-list'),
    path('audit-sessions/<int:session_id>/add-items/', add_items_manual, name='item-add'),
    path('audit-sessions/<int:session_id>/remove-items/', remove_items, name='item-remove'),
    
    # Item detail & actions
    path('audit-items/<int:pk>/', AuditItemDetailView.as_view(), name='item-detail'),
    path('audit-items/<int:pk>/check/', check_item, name='item-check'),
    path('audit-items/<int:pk>/mark-missing/', mark_missing, name='item-mark-missing'),
]
