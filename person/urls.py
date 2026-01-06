"""Person URLs - Dev A"""
from django.urls import path
from .views import PersonListView, PersonDetailView

app_name = 'person'

urlpatterns = [
    path('', PersonListView.as_view(), name='list'),
    path('<int:pk>/', PersonDetailView.as_view(), name='detail'),
]
