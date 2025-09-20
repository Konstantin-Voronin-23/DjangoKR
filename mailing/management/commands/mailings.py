import logging
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from ...models import Mailing, MailingAttempt

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Запускает все активные рассылки"

    def handle(self, *args, **options):
        now = timezone.now()
        self.stdout.write(f"Запуск обработки рассылок в {now}")

        mailings_to_send = Mailing.objects.filter(
            status="started", start_time__lte=now, end_time__gte=now
        )

        self.stdout.write(f"Найдено рассылок: {mailings_to_send.count()}")
        for mailing in mailings_to_send:
            self.stdout.write(f"Рассылка ID: {mailing.id}, Статус: {mailing.status}")
            self.stdout.write(f"Время начала: {mailing.start_time}")
            self.stdout.write(f"Время окончания: {mailing.end_time}")
            self.stdout.write(f"Клиентов: {mailing.clients.count()}")

        if not mailings_to_send:
            self.stdout.write("Нет активных рассылок для отправки.")
            return

        total_sent = 0
        total_failed = 0

        for mailing in mailings_to_send:
            self.stdout.write(
                f'Обрабатывается рассылка #{mailing.id} "{mailing.message.subject}"'
            )

            for client in mailing.clients.all():
                try:
                    result = send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )

                    status = "success"
                    server_response = "Успешно отправлено"
                    total_sent += 1
                    self.stdout.write(f"  ✓ Письмо для {client.email} отправлено.")

                except Exception as e:
                    status = "failed"
                    server_response = str(e)
                    total_failed += 1
                    self.stdout.write(f"  ✗ Ошибка для {client.email}: {e}")
                    logger.error(f"Ошибка отправки письма: {e}")

                MailingAttempt.objects.create(
                    mailing=mailing, status=status, server_response=server_response
                )

            if mailing.end_time <= now:
                mailing.status = "completed"
                mailing.save()
                self.stdout.write(f"  Рассылка #{mailing.id} завершена (время истекло)")

        self.stdout.write(
            self.style.SUCCESS(
                f"Обработка завершена. Успешно: {total_sent}, Неудачно: {total_failed}"
            )
        )
