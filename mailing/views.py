from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_page


@cache_page(60)
def cache_test_view(request):
    """ Тестовая страница для проверки кэширования.
    Возвращает текущее время, страница кэшируется на 60 секунд """

    from django.http import HttpResponse
    from django.utils import timezone

    return HttpResponse(f"Время генерации страницы: {timezone.now()}")


def home(request):
    """ Главная страница приложения рассылок.
    Показывает общую статистику: количество рассылок, активных рассылок и уникальных клиентов """

    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="started").count()
    unique_clients = Client.objects.values("email").distinct().count()

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_clients": unique_clients,
    }
    return render(request, "mailing/home.html", context)


class ClientListView(LoginRequiredMixin, ListView):
    """ Список клиентов.
    Показывает всех клиентов для администраторов или только своих для обычных пользователей """

    model = Client

    def get_queryset(self):
        """Фильтрует клиентов в зависимости от прав пользователя."""

        if self.request.user.has_perm("mailing.view_all_clients"):
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    """ Создание нового клиента.
    Автоматически назначает текущего пользователя владельцем клиента """

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        """Устанавливает владельца клиента перед сохранением"""

        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Передает запрос в форму для дополнительной валидации"""

        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование клиента.
    Разрешает редактирование только своих клиентов или всех для администраторов """

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def get_queryset(self):
        """Фильтрует клиентов в зависимости от прав пользователя"""

        if self.request.user.has_perm("mailing.view_all_clients"):
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        """Передает запрос в форму для дополнительной валидации"""

        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление клиента.
    Разрешает удаление только своих клиентов или всех для администраторов """

    model = Client
    success_url = reverse_lazy("mailing:client_list")

    def get_queryset(self):
        """Фильтрует клиентов в зависимости от прав пользователя"""

        if self.request.user.has_perm("mailing.view_all_clients"):
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    """ Список сообщений.
    Показывает все сообщения для администраторов или только свои для обычных пользователей """

    model = Message

    def get_queryset(self):
        """Фильтрует сообщения в зависимости от прав пользователя"""

        if self.request.user.has_perm("mailing.view_all_messages"):
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    """ Создание нового сообщения.
    Автоматически назначает текущего пользователя владельцем сообщения """

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        """Устанавливает владельца сообщения перед сохранением"""

        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Передает запрос в форму для дополнительной валидации"""

        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование сообщения.
    Разрешает редактирование только своих сообщений или всех для администраторов """

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        """Фильтрует сообщения в зависимости от прав пользователя"""

        if self.request.user.has_perm("mailing.view_all_messages"):
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        """Передает запрос в форму для дополнительной валидации"""

        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление сообщения.
    Разрешает удаление только своих сообщений или всех для администраторов"""

    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        """Фильтрует сообщения в зависимости от прав пользователя"""

        if self.request.user.has_perm("mailing.view_all_messages"):
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MailingListView(LoginRequiredMixin, ListView):
    """ Список рассылок.
    Показывает все рассылки для администраторов или только свои для обычных пользователей """

    model = Mailing

    def get_queryset(self):
        """Фильтрует рассылки в зависимости от прав пользователя"""

        if self.request.user.has_perm("mailing.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    """ Создание новой рассылки.
    Автоматически назначает текущего пользователя владельцем рассылки """

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        """Устанавливает владельца рассылки перед сохранением"""

        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Передает запрос в форму для дополнительной валидации"""

        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование рассылки.
    Разрешает редактирование только своих рассылок или всех для администраторов """

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def get_queryset(self):
        """Фильтрует рассылки в зависимости от прав пользователя"""

        if self.request.user.has_perm("mailing.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        """Передает запрос в форму для дополнительной валидации"""

        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление рассылки.
    Разрешает удаление только своих рассылок или всех для администраторов """

    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def get_queryset(self):
        """Фильтрует рассылки в зависимости от прав пользователя"""

        if self.request.user.has_perm("mailing.view_all_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    """ Список попыток рассылок со статистикой.
    Показывает статистику успешных и неудачных попыток отправки """

    model = MailingAttempt
    template_name = "mailing/attempt_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        """Фильтрует попытки рассылок в зависимости от прав пользователя"""

        if self.request.user.has_perm("mailing.view_all_mailings"):
            return MailingAttempt.objects.all().select_related("mailing")
        return MailingAttempt.objects.filter(
            mailing__owner=self.request.user
        ).select_related("mailing")

    def get_context_data(self, **kwargs):
        """ Добавляет статистику в контекст: общее количество попыток|успешные и неудачные попытки|процент успеха|
        статистика по каждой рассылке """

        context = super().get_context_data(**kwargs)

        attempts = self.get_queryset()

        context["total_attempts"] = attempts.count()
        context["successful_attempts"] = attempts.filter(status="success").count()
        context["failed_attempts"] = attempts.filter(status="failed").count()
        context["success_rate"] = (
            (context["successful_attempts"] / context["total_attempts"] * 100)
            if context["total_attempts"] > 0
            else 0
        )

        mailing_stats = []
        mailings = Mailing.objects.filter(attempts__isnull=False).distinct()

        for mailing in mailings:
            mailing_attempts = attempts.filter(mailing=mailing)
            mailing_stats.append(
                {
                    "mailing": mailing,
                    "total": mailing_attempts.count(),
                    "success": mailing_attempts.filter(status="success").count(),
                    "failed": mailing_attempts.filter(status="failed").count(),
                }
            )

        context["mailing_stats"] = mailing_stats

        return context


@login_required
def start_mailing(request, pk):
    """
    Запуск рассылки вручную.
    Изменяет статус рассылки на 'started' и запускает процесс отправки.
    Проверяет права пользователя на запуск данной рассылки
    """

    mailing = get_object_or_404(Mailing, pk=pk)

    if not (
        request.user == mailing.owner
        or request.user.has_perm("mailing.view_all_mailings")
    ):
        messages.error(request, "У вас нет прав для запуска этой рассылки")
        return redirect("mailing:mailing_list")

    mailing.status = "started"
    mailing.save()
    messages.success(request, f'Рассылка "{mailing.message.subject}" запущена!')

    return redirect("mailing:mailing_list")
