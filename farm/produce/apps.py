"""Application configuration for the produce app. It declares the inventory module so Django can include it in the project."""

from django.apps import AppConfig


class ProduceConfig(AppConfig):
    name = 'produce'
