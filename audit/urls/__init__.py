# Audit URLs
from django.urls import path, include
from . import session_urls, item_urls, action_urls

app_name = 'audit'

urlpatterns = [
    path('audit-sessions/', include(session_urls)),
    path('', include(item_urls)),
    path('', include(action_urls)),
]
