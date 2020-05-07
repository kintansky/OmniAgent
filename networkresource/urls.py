from django.urls import path
from . import views

urlpatterns = [
    path('ip/', views.ip_list, name='ip_record'),
    path('ip/search/', views.search_ip, name='search_ip'),
    path('ip/download/', views.export_ip, name='export_ip'),
    # 分配台账
    path('ip/allocate/', views.new_allocate_ip, name='new_ip_allocate'),
    path('ip/allocate/ajax_get_olt_can_allocated_ip/', views.ajax_get_olt_can_allocated_ip, name='ajax_get_olt_can_allocated_ip'),
    path('ip/allocate/generate_ip2/', views.ajax_generate_ip_list2, name='generate_ip2'),
    path('ip/allocate/confirm_ready_ip/', views.confirm_ready_ip, name='confirm_ready_ip'),
    path('ip/allocate/remove_conf_ip/', views.remove_conf_ip, name='remove_conf_ip'),
    path('ip/allocate/get_olt_bng/<str:device_type>/', views.ajax_get_olt_bng, name='get_olt_bng'),
    path('ip/allocate/parse_icp/', views.parse_icp, name='parse_icp'),
    path('ip/allocate/confirm_icp/', views.confirm_icp, name='confirm_icp'),
    path('ip/locate_icp/', views.ajax_locate_icp, name='ajax_locate_icp'),
    path('ip/mod_icp/<str:operation_type>', views.ajax_mod_icp_info, name='ajax_mod_icp_info'),
    path('ip/allocate/confirm/', views.ajax_confirm_allocate, name='confirm_allocate'),
    path('ip/allocated_client_list/', views.ip_allocated_client_list, name='ip_allocated_client_list'),
    path('ip/allocated_client_search/', views.allocated_client_search, name='allocated_client_search'),
    path('ip/allocated_ip_list/', views.ip_allocated_list, name='ip_allocated_list'),
    path('ip/allocated_ip_search/', views.ip_allocated_search, name='ip_allocates_search'),
    path('ip/locate_allocated_ip/', views.ajax_locate_allocated_ip, name='locate_allocated_ip'),
    path('ip/mod_allocated_ip/<str:operation_type>', views.ajax_mod_allocated_ip, name='mod_allocated_ip'),
    path('ip/export_ip_allocation/<str:amount>', views.export_ip_allocation, name='export_ip_allocation'),

    path('ajax_search_slot_ports/', views.ajax_search_slot_ports, name='ajax_search_slot_ports'),
    # 在用网段情况
    path('ip/list_all_ip_segment/', views.list_all_ip_segment, name='list_all_ip_segment'),
    path('ip/list_all_ip_segment/search', views.search_all_ip_segment, name='search_all_ip_segment'),
    path('ip/list_all_ip_segment/ajax_confirm_new_segment/', views.ajax_confirm_new_segment, name='ajax_confirm_new_segment'),
    path('ip/list_all_ip_segment/ajax_turn_segment_state/<str:operation_type>', views.ajax_turn_segment_state, name='ajax_turn_segment_state'),

    # 网段规划
    path('ip/segment_schema/', views.list_all_segment, name='list_all_segment'),
    path('ip/segment_schema/ajax_allocate_segment/', views.allocate_segment, name='ajax_allocate_segment'),
    path('ip/segment_schema/search/', views.search_segment, name='search_segment'),
    path('ip/segment_schema/detail/', views.schema_detail, name='schema_detail'),
    path('ip/segment_schema/get_schema_olt_bng/<str:device_type>', views.get_schema_olt_bng, name='get_schema_olt_bng'),
    path('ip/segment)schema/confirm_segment_to_draft/', views.confirm_segment_to_draft, name='confirm_segment_to_draft'),
    path('ip/segment)schema/confirm_draft/', views.confirm_draft, name='confirm_draft'),

    # IP资源使用情况
    path('ip/ip_allocated_segment/', views.get_device_allocated_segment, name='get_device_allocated_segment'),
    path('ip/ip_allocated_segment/search/', views.search_device_allocated_segment, name='search_device_allocated_segment'),
    path('ip/ip_allocated_segment/get_segment_used_detail/', views.ajax_get_segment_used_detail, name='ajax_get_segment_used_detail'),
    path('ip/ip_allocated_segment/get_segment_left_cnt/', views.ajax_get_segment_left_cnt, name='ajax_get_segment_left_cnt'),
    path('ip/ip_allocated_segment/reserve_segment/', views.reserve_segment, name='reserve_segment'),
    path('ip/ip_allocated_segment/cancle_reserve/', views.cancle_reserve, name='cancle_reserve'),
    path('ip/ip_allocated_segment/delay_reserve/', views.delay_reserve, name='delay_reserve'),
    path('ip/ip_allocated_segment/get_my_reserved_list/', views.ajax_get_my_reserved_list, name='ajax_get_my_reserved_list'),

    # 开通工作量情况统计
    path('ip/allocate/workload/', views.list_workload, name='list_workload'),
    
]