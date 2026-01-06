"""Ticket URLs - Dev D1"""
from django.urls import path
from ..views import (
    TicketListView, TicketDetailView,
    approve_ticket, reject_ticket, complete_ticket
)

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:pk>/approve/', approve_ticket, name='ticket-approve'),
    path('<int:pk>/reject/', reject_ticket, name='ticket-reject'),
    path('<int:pk>/complete/', complete_ticket, name='ticket-complete'),
]
