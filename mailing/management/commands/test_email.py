from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Тестирование отправки email"

    def handle(self, *args, **options):
        try:
            result = send_mail(
                subject='Тестовое письмо',
                message='Это тестовое письмо из Django',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['heavensmiting@gmail.com'],  # ваш email для теста
                fail_silently=False,
            )
            self.stdout.write(f"Результат отправки: {result}")
        except Exception as e:
            self.stdout.write(f"Ошибка: {e}")
