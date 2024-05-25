from django.shortcuts import render

# Create your views here.
import random

from django.db.models import Func
from django.views.generic import DetailView, ListView

from blog.models import Blog
from mailings.models import Mailing, Client


# Create your views here.
class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class RandomFunc(Func):
    function = 'RANDOM'


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = len(Mailing.objects.all())
        mailings_is_active = len(Mailing.objects.filter(is_active=True))
        unique_clients_count = Client.objects.values('email').distinct().count()
        context['mailings'] = mailings
        context['mailings_is_active'] = mailings_is_active
        context['unique_clients_count'] = unique_clients_count
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:3]