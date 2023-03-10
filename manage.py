#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main(arg):
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pelican.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if arg == ['manage.py', 'runserver']:
        arg.append('0.0.0.0:8000')
    execute_from_command_line(arg)


if __name__ == '__main__':
    main(sys.argv)
