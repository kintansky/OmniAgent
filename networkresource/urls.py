from django.urls import path
from . import views

urlpatterns = [
    path('ip/', views.ip_list, name='ip_record'),
    path('ip/search/', views.search_ip, name='search_ip'),
    path('ip/download/', views.export_ip, name='export_ip'),
    path('ip/<str:ip_type>/allocate/', views.allocate_ip, name='allocate_ip'),
    # new ip allocate
    path('ip/allocate/', views.new_allocate_ip, name='new_ip_allocate'),
    path('ip/allocate/generate_ip/', views.ajax_generate_ip_list, name='generate_ip'),
    path('ip/allocate/remove_ip/', views.ajax_remove_ip, name='remove_ip'),
    path('ip/allocate/get_bng/', views.ajax_get_bng, name='get_bng'),
    path('ip/allocate/confirm/', views.ajax_confirm_allocate, name='confirm_allocate'),

    path('allocated_ip/<str:ip_type>/', views.allocate_ip_list, name='allocated_ip_list'),
    path('allocated_ip/<str:ip_type>/search/', views.search_allocated_ip, name='search_allocated_ip'),
    path('ajax_locate_ip/<str:ip_type>/', views.ajax_locate_ip, name='ajax_locate_ip'),
    path('ip_alocation_mod/<str:ip_type>/', views.ip_allocation_mod, name='ip_allocation_mod'),
    path('ajax_search_slot_ports/', views.ajax_search_slot_ports, name='ajax_search_slot_ports'),
]