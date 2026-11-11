"""Application configuration for the suppliers app. It loads the supplier module so the project can track vendor relationships."""

from django.apps import AppConfig


class SuppliersConfig(AppConfig):
    name = 'suppliers'
