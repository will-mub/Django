from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.expense_create, name='expense_create'),
    path('edit/<int:pk>/', views.expense_update, name='expense_update'),
    path('void/<int:pk>/', views.expense_void, name='expense_void'),
]