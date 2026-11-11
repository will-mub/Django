"""URL routes for the produce app. The routes connect inventory pages to the CRUD operations used by farm staff."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.produce_list, name='produce_list'),

    path('add/', views.produce_create, name='produce_create'),

    path('edit/<int:pk>/', views.produce_update,
         name='produce_update'),

    path('delete/<int:pk>/', views.produce_delete,
         name='produce_delete'),
]