"""Application configuration for the customers app. This tells Django how to load the customer management module in the farm project."""

from django.apps import AppConfig


class CustomersConfig(AppConfig):
    name = 'customers'
