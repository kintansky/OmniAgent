from django.urls import path
from . import views

urlpatterns = [
    path('moudle/', views.moudle_list, name='moudle_list'),
    path('moudle/search/', views.search_moudle, name='search_moudle'),
    path('moudle/download/', views.export_moudle, name='export_moudle'),
    path('porterror/', views.port_error_list, name='port_error_list'),
]