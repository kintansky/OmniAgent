from django.urls import path
from . import views

urlpatterns = [
    path('', views.ip_list, name='ip_record'),
    path('search/', views.search_ip, name='search_ip'),
]