from django.urls import path
from . import views

urlpatterns = [
    path('ip/', views.ip_list, name='ip_record'),
    path('ip/search/', views.search_ip, name='search_ip'),
    path('ip/download/', views.export_ip, name='export_ip'),
    # new ip allocate
    path('ip/allocate/', views.new_allocate_ip, name='new_ip_allocate'),
    path('ip/allocate/generate_ip/', views.ajax_generate_ip_list, name='generate_ip'),
    path('ip/allocate/remove_ip/', views.ajax_remove_ip, name='remove_ip'),
    path('ip/allocate/get_olt_bng/<str:device_type>/', views.ajax_get_olt_bng, name='get_olt_bng'),
    path('ip/allocate/confirm/', views.ajax_confirm_allocate, name='confirm_allocate'),
    path('ip/allocated_ip_list/', views.ip_allocated_list, name='ip_allocated_list'),
    path('ip/allocated_ip_search/', views.ip_allocated_search, name='ip_allocates_search'),
    path('ip/locate_allocated_ip/', views.ajax_locate_allocated_ip, name='locate_allocated_ip'),
    path('ip/mod_allocated_ip/', views.ajax_mod_allocated_ip, name='mod_allocated_ip'),

    path('ajax_search_slot_ports/', views.ajax_search_slot_ports, name='ajax_search_slot_ports'),
]