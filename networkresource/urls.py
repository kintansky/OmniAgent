from django.urls import path
from . import views

urlpatterns = [
    path('ip/', views.ip_list, name='ip_record'),
    path('ip/search/', views.search_ip, name='search_ip'),
    path('ip/download/', views.export_ip, name='export_ip'),
    path('ip/<str:ip_type>/allocate/', views.allocate_ip, name='allocate_ip'),

    path('allocated_ip/<str:ip_type>/', views.allocate_ip_list, name='allocated_ip_list'),
    path('allocated_ip/<str:ip_type>/search/', views.search_allocated_ip, name='search_allocated_ip'),
    path('ajax_locate_ip/<str:ip_type>/', views.ajax_locate_ip, name='ajax_locate_ip'),
    path('ip_alocation_mod/<str:ip_type>/', views.ip_allocation_mod, name='ip_allocation_mod'),
    path('ajax_search_slot_ports/', views.ajax_search_slot_ports, name='ajax_search_slot_ports'),
]