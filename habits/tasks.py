from celery import shared_task
from habits.models import Habit
from habits.services import send_telegram_message
import pytz
from django.conf import settings
from datetime import datetime, timedelta


@shared_task()
def telegram_notification():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_time = datetime.now(zone)
    current_time_less = current_time - timedelta(minutes=1)
    habits = Habit.objects.filter(time__lte=(current_time + timedelta(minutes=1)).time(),
                                  time__gte=current_time_less.time())
    for habit in habits:
        user_tg = habit.user.tg_chat_id
        message = f"Я буду {habit.action} в {habit.time} в {habit.place}"
        send_telegram_message(message, user_tg)
