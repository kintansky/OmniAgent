"""
WSGI config for omni project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 生产环境使用settings内的production配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omni.settings.production')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omni.settings')

application = get_wsgi_application()
