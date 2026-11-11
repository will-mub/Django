"""URL routes for the dashboard app. The root route shows the farm overview page for the application homepage."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
]