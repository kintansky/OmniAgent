#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    # 调试环境使用development的配置文件
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omni.settings.development')
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omni.settings')
    # py manage.py runserver --settings omni.settings.development
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
