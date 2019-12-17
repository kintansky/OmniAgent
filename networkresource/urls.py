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
    path('ip/allocated_client_list/', views.ip_allocated_client_list, name='ip_allocated_client_list'),
    path('ip/allocated_client_search/', views.allocated_client_search, name='allocated_client_search'),
    path('ip/allocated_ip_list/', views.ip_allocated_list, name='ip_allocated_list'),
    path('ip/allocated_ip_search/', views.ip_allocated_search, name='ip_allocates_search'),
    path('ip/locate_allocated_ip/', views.ajax_locate_allocated_ip, name='locate_allocated_ip'),
    path('ip/mod_allocated_ip/<str:operation_type>', views.ajax_mod_allocated_ip, name='mod_allocated_ip'),

    path('ajax_search_slot_ports/', views.ajax_search_slot_ports, name='ajax_search_slot_ports'),

    path('ip/ip_allocated_segment/', views.get_device_allocated_segment, name='get_device_allocated_segment'),
    path('ip/ip_allocated_segment/search/', views.search_device_allocated_segment, name='search_device_allocated_segment'),
    path('ip/ip_allocated_segment/get_segment_used_detail/', views.ajax_get_segment_used_detail, name='ajax_get_segment_used_detail'),
    path('ip/ip_allocated_segment/get_segment_left_cnt/', views.ajax_get_segment_left_cnt, name='ajax_get_segment_left_cnt'),
    path('ip/ip_allocated_segment/reserve_segment/', views.reserve_segment, name='reserve_segment'),
    path('ip/ip_allocated_segment/cancle_reserve/', views.cancle_reserve, name='cancle_reserve'),
    path('ip/ip_allocated_segment/get_my_reserved_list/', views.ajax_get_my_reserved_list, name='ajax_get_my_reserved_list')
]