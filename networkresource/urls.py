from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_ports, name='port_resource_empty'),
    path('search/', views.search_device_ports, name='port_resource'),
]