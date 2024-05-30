from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView

from mailings.forms import CreateMailingForm, UpdateMailingForm, CreateClientForm, CreateMessageForm
from mailings.models import Mailing, Client, MailingLog, Message


# Create your views here.

@method_decorator(login_required(login_url='users:login'), name='dispatch')
class CreateMailingView(CreateView):
    model = Mailing
    form_class = CreateMailingForm
    success_url = reverse_lazy('mailings:list_mailing')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get(self, request, **kwargs):
        user = self.request.user
        form = self.form_class(self.request.user, request.POST)
        context = {
            'form': form,
        }
        clients = Client.objects.filter(user=user)
        message = Message.objects.filter(user=user)
        context['clients'] = clients
        context['message'] = message
        return render(request, 'mailings/mailing_form.html', context)



    def save_mailing(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.user = self.request.user
            mailing.save()
            form.save_m2m()
        return redirect(self.success_url)


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class UpdateMailingView(UpdateView):
    model = Mailing
    form_class = UpdateMailingForm
    success_url = reverse_lazy('mailings:list_mailing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = Client.objects.filter(user=self.request.user)
        context['clients'] = clients
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class ListMailingView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'

    def get_queryset(self):
        return Mailing.objects.filter(user=self.request.user)


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class DetailMailingView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class DeleteMailingView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:list_mailing')


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class CreateClientView(CreateView):
    model = Client
    form_class = CreateClientForm
    success_url = reverse_lazy('mailings:list_client')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                client = form.save(commit=False)
                client.user = self.request.user
                client.save()
            except ValueError:
                return render(request, 'mailings/client_exists.html')
            else:
                return redirect(self.success_url)


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class UpdateClientView(UpdateView):
    model = Client
    form_class = CreateClientForm
    success_url = reverse_lazy('mailings:list_client')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.filter(user=self.request.user)
        return context


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class ListClientView(ListView):
    model = Client
    template_name = 'mailings/clients_list.html'

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class DetailClientView(DetailView):
    model = Client
    template_name = 'mailings/client_detail.html'


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class DeleteClientView(DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:clients_list')


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class MailingLogListView(ListView):
    model = MailingLog
    template_name = 'mailings/mailing_logs_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all
        else:
            return self.model.objects.filter(user=self.request.user)


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class DetailMailingLogView(DetailView):
    model = MailingLog
    template_name = 'mailings/mailing_log_detail.html'


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class DeleteMailingLogView(DeleteView):
    model = MailingLog
    template_name = 'mailings/log_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_logs_list')


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class CreateMessageView(CreateView):
    model = Message
    form_class = CreateMessageForm
    success_url = reverse_lazy('mailings:list_message')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.user = self.request.user
            message.save()
        return redirect(self.success_url)


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class ListMessageView(ListView):
    model = Message
    template_name = 'mailings/messages_list.html'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class UpdateMessageView(UpdateView):
    model = Message
    form_class = CreateMessageForm
    success_url = reverse_lazy('mailings:list_message')


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class DeleteMessageView(DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:list_message')


@method_decorator(login_required(login_url='users:login'), name='dispatch')
class DetailMessageView(DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
