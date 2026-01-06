"""
AuditSession URLs
=================

Người phụ trách: [Dev C1]

Base path: /api/audit-sessions/
"""

from django.urls import path
from ..views import (
    AuditSessionListView,
    AuditSessionDetailView,
    generate_items,
    start_session,
    complete_session,
    export_report,
)

urlpatterns = [
    # List & Create
    path('', AuditSessionListView.as_view(), name='session-list'),
    
    # Detail, Update, Delete
    path('<int:pk>/', AuditSessionDetailView.as_view(), name='session-detail'),
    
    # Actions
    path('<int:pk>/generate-items/', generate_items, name='session-generate-items'),
    path('<int:pk>/start/', start_session, name='session-start'),
    path('<int:pk>/complete/', complete_session, name='session-complete'),
    path('<int:pk>/report/', export_report, name='session-report'),
]
