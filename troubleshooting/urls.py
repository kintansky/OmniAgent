from django.urls import path
from . import views

urlpatterns = [
    path('link_utilization/', views.link_utilization, name='link_utilization'),
    path('link_utilization/get_bng/', views.ajax_get_bng, name='ajax_get_bng'),
    path('link_utilization/get_link_utilization/', views.get_link_utilization, name='get_link_utilization'),
]