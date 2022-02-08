from __future__ import absolute_import, unicode_literals
from corner_test.celery import app
from datetime import datetime
from django.conf import settings
from corner_test.apps.menus.models import Menu
from corner_test.apps.menus.serializers import MenuSerializer
from corner_test.apps.utils.slack import SlackService


@app.task
def send_today_menu():
    service = SlackService(settings.SLACK_API_KEY)
    today = datetime.now().date()
    try:
        menu = Menu.objects.get(date=today)
        menu_data = MenuSerializer(menu).data
    except Exception as e:
        menu_data = {"options": ["no menu today, yet"]}
    users = service.get_users_info()
    service.send_messages(users, menu_data)


@app.task
def save_messages():
    service = SlackService(settings.SLACK_API_KEY)
    service.get_messages()
