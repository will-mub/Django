"""Concept and purpose for this file. This module belongs to the farm management application and supports the core business workflow of the project."""

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Point Django to the project's default settings file.    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm.settings')
    try:
        # Import Django's command line execution function         
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Provide a helpful error message ìf Django isn't installed or activated.        
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        # Execute the command passed via the terminal.
    execute_from_command_line(sys.argv)

# Ensure main() only runs when this script is executed directly, not when imported 
if __name__ == '__main__':
    main()
