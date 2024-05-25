from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView
from django.views.decorators.cache import cache_page
app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('view/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='view'),
]