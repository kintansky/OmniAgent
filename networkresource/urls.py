from django.urls import path
from . import views

urlpatterns = [
    path('port/', views.show_ports, name='port_resource_empty'),
    path('port/search/', views.search_device_ports, name='port_resource'),
    path('ip/', views.ip_list, name='ip_record'),
    path('ip/search/', views.search_ip, name='search_ip'),
    path('ip/download/', views.export_ip, name='export_ip'),
    path('ip/<str:ip_type>/allocate/', views.allocate_ip, name='allocate_ip'),
    path('allocated_ip/<str:ip_type>/', views.allocate_ip_list, name='allocated_ip_list'),
    path('allocated_ip/<str:ip_type>/search/', views.search_allocated_ip, name='search_allocated_ip'),
]