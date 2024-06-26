from django import forms

from mailings.models import Mailing, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'clients':
                continue
            elif field_name == 'message':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'


class CreateMessageForm(StyleFormMixin, forms.ModelForm):
    mail_subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите текст'}),
        label='Тема сообщения'
    )

    mail_text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Введите текст'}),
        label='Текст сообщения'
    )

    class Meta:
        model = Message
        fields = ('mail_subject', 'mail_text',)


class CreateMailingForm(StyleFormMixin, forms.ModelForm):
    mailing_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }
        ),
        label='Дата и время рассылки'
    )

    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label='Клиенты'
    )

    message = forms.ModelChoiceField(
        queryset=Message.objects.none(),
        widget=forms.Select(),
        label='Сообщение'
    )

    class Meta:
        model = Mailing
        exclude = ('status', 'user', 'is_active')

    def __init__(self, user, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(user=user)
        self.fields['message'].queryset = Message.objects.filter(user=user)


class UpdateMailingForm(StyleFormMixin, forms.ModelForm):

    mailing_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }
        ),
        label='Дата и время рассылки'
    )

    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label='Клиенты'
    )

    message = forms.ModelChoiceField(
        queryset=Message.objects.none(),
        label='Сообщение'
    )

    class Meta:
        model = Mailing
        fields = ('mailing_time', 'frequency', 'clients')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(user=user)
        self.fields['message'].queryset = Message.objects.filter(user=user)


class CreateClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('user', )


class ManagerMailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('is_active',)
