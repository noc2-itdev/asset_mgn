# Asset App - URLs
from django.urls import path, include
from . import asset_urls, component_urls, transfer_urls

app_name = 'asset'

urlpatterns = [
    path('assets/', include(asset_urls)),
    path('assets/', include(component_urls)),
    path('assets/', include(transfer_urls)),
]
