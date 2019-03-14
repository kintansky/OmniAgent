from django.urls import path
from . import views

urlpatterns = [
    path('port/', views.show_ports, name='port_resource_empty'),
    path('port/search/', views.search_device_ports, name='port_resource'),
    path('ip/', views.ip_list, name='ip_record'),
    path('ip/search/', views.search_ip, name='search_ip'),
    path('ip/download/', views.export_ip, name='export_ip'),
    path('ip/public/allocate/', views.allocate_public_ip, name='allocate_public_ip'),
    path('ip/private/allocate/', views.allocate_private_ip, name='allocate_private_ip'),
    path('allocated_ip/public/', views.allocate_public_ip_list, name='allocated_public_ip_list'),
    path('allocated_ip/public/search/', views.search_allocate_public_ip, name='allocated_public_ip_search'),
    path('allocated_ip/private/', views.allocate_private_ip_list, name='allocated_private_ip_list'),
    path('allocated_ip/private/search/', views.search_allocate_private_ip, name='allocated_private_ip_search'),
]