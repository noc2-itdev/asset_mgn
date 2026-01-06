# Audit App - URLs
# Tổng hợp tất cả URL patterns từ các module con

from django.urls import path, include

from . import session_urls
from . import item_urls
from . import action_urls

app_name = 'audit'

urlpatterns = [
    # AuditSession endpoints
    path('audit-sessions/', include(session_urls)),
    
    # AuditItem endpoints  
    path('', include(item_urls)),
    
    # AuditAction endpoints
    path('', include(action_urls)),
]
