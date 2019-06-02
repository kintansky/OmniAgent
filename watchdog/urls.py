from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('add_device/', views.add_device, name='add_device'),
    path('search/', views.search_device, name='search_device'),
    path('detail/<str:device_name>', views.device_detail, name='device_detail'),
]