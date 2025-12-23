from django.urls import path
from . import views

urlpatterns = [
    # Department URLs
    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),

    # Person URLs
    path('persons/', views.PersonListCreateView.as_view(), name='person-list-create'),
    path('persons/<int:pk>/', views.PersonDetailView.as_view(), name='person-detail'),

    # Location URLs
    path('locations/', views.LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', views.LocationDetailView.as_view(), name='location-detail'),

    # Asset Category URLs
    path('categories', views.AssetCategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.AssetCategoryDetailView.as_view(), name='category-detail'),

    # Asset Attachment URLs
    path('attachments', views.AssetAttachmentListCreateView.as_view(), name='attachment-list-create'),
    path('attachments/<int:pk>/', views.AssetAttachmentDetailView.as_view(), name='attachment-detail'),

    # Asset URLs
    path('assets/', views.AssetListCreateView.as_view(), name='asset-list-create'),
    path('assets/<int:pk>/', views.AssetDetailView.as_view(), name='asset-detail'),
    path('assets/<int:pk>/components/', views.AssetComponentsView.as_view(), name='asset-components'),
    path('assets/<int:pk>/transfer/', views.transfer_asset, name='asset-transfer'),
    path('assets/<int:pk>/upgrade/', views.upgrade_component, name='asset-upgrade'),
    path('assets/<int:pk>/history/', views.AssetHistoryListView.as_view(), name='asset-history'),

    # Ticket Request URLs (thay thế Repair Request)
    path('ticket-requests', views.TicketRequestListCreateView.as_view(), name='ticket-request-list-create'),
    path('ticket-requests/<int:pk>/', views.TicketRequestDetailView.as_view(), name='ticket-request-detail'),

    # Asset Audit URLs
    path('audits', views.AssetAuditListCreateView.as_view(), name='audit-list-create'),

    # Statistics and additional endpoints
    path('statistics', views.asset_statistics, name='asset-statistics'),
    path('locations/list/', views.get_locations, name='get-locations'),
    path('assets/qr/<str:asset_code>/', views.asset_qr_lookup, name='asset-qr-lookup'),
]
