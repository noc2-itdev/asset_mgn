"""Session URLs - Dev C1"""
from django.urls import path
from ..views import (
    AuditSessionListView, AuditSessionDetailView,
    generate_items, start_session, complete_session, export_report
)

urlpatterns = [
    path('', AuditSessionListView.as_view(), name='session-list'),
    path('<int:pk>/', AuditSessionDetailView.as_view(), name='session-detail'),
    path('<int:pk>/generate-items/', generate_items, name='session-generate'),
    path('<int:pk>/start/', start_session, name='session-start'),
    path('<int:pk>/complete/', complete_session, name='session-complete'),
    path('<int:pk>/report/', export_report, name='session-report'),
]
