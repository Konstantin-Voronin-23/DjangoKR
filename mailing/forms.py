from django import forms
from .models import Client, Message, Mailing


class ClientForm(forms.ModelForm):
    """Класс создания формы клиента"""

    class Meta:
        model = Client
        fields = ["email", "full_name", "comment"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Введите email"}
            ),
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите ФИО"}
            ),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Комментарий", "rows": 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                field.widget.attrs.get("class", "") + " form-control"
            )


class MessageForm(forms.ModelForm):
    """Класс создания формы сообщения"""

    class Meta:
        model = Message
        fields = ["subject", "body"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request:
            instance.owner = self.request.user
        if commit:
            instance.save()
        return instance


class MailingForm(forms.ModelForm):
    """Класс создания формы рассылки"""

    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "clients"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "clients": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields["message"].queryset = Message.objects.filter(
                owner=self.request.user
            )
            self.fields["clients"].queryset = Client.objects.filter(
                owner=self.request.user
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request:
            instance.owner = self.request.user
        if commit:
            instance.save()
            self.save_m2m()
        return instance
