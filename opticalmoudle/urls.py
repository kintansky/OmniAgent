from django.urls import path
from . import views

urlpatterns = [
    path('', views.moudle_list, name='moudle_list'),
    path('search/', views.search_moudle, name='search_moudle'),
]