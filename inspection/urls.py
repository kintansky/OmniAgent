from django.urls import path
from . import views

urlpatterns = [
    path('moudle/', views.moudle_list, name='moudle_list'),
    path('moudle/search/', views.search_moudle, name='search_moudle'),
    path('moudle/download/', views.export_moudle, name='export_moudle'),
    
    path('porterror/', views.port_error_list, name='port_error_list'),
    path('porterror/search/', views.search_port_error, name='search_port_error'),
    path('porterror/download/', views.export_porterror, name='export_porterror'),
    path('porterror/ajax_search_error_effect/', views.ajax_search_error_effect, name='ajax_search_error_effect'),
    path('porterror/ajax_port_operation_list/<str:path_type>', views.ajax_port_operation_list, name='ajax_port_error_operation_list'),
    path('porterror/ajax_port_operate/<str:operation_type>', views.ajax_port_operate, name='ajax_port_error_operate'),
    path('porterror/fixrecord/', views.porterror_fix_list, name='port_error_fix_list'),
    path('porterror/fixrecord/search/', views.search_porterror_fix, name='search_porterror_fix'),
    path('porterror/fixrecord/download/', views.export_porterrorfix, name='export_porterrorfix'),
    path('porterror/my_tasks/', views.my_port_error_tasks, name='my_port_error_tasks'),

    path('oneway/', views.oneway_list, name='oneway_list'),
    path('oneway/search/', views.search_oneway, name='search_oneway'),
    path('oneway/download/', views.export_oneway, name='export_oneway'),
    path('oneway/tag/', views.tag_oneway_device, name='tag_oneway'),
    path('oneway/tag/cancle/', views.cancle_tag_oneway, name='cancle_tag_oneway'),

    path('group_client_list/', views.group_client_list, name='group_client_list'),
    path('group_client_list/search/', views.search_group_client, name='search_group_client'),

    path('natpool/', views.natpool_list, name='natpool_list'),
    path('natpool/search/', views.search_natpool, name='search_natpool'),
    path('natpool/download/', views.export_natpool, name='export_natpool'),
]