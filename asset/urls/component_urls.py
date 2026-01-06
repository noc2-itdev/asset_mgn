"""Component URLs - Dev B2"""
from django.urls import path
from ..views import AssetComponentListView, upgrade_component, retrieve_component

urlpatterns = [
    path('<int:pk>/components/', AssetComponentListView.as_view(), name='asset-components'),
    path('<int:pk>/upgrade/', upgrade_component, name='asset-upgrade'),
    path('<int:pk>/retrieve/', retrieve_component, name='asset-retrieve'),
]
