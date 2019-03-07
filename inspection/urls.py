from django.urls import path
from . import views

urlpatterns = [
    path('moudle/', views.moudle_list, name='moudle_list'),
    path('moudle/search/', views.search_moudle, name='search_moudle'),
]