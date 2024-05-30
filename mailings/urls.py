from django.urls import path

from mailings.views import CreateMailingView, ListMailingView, UpdateMailingView, DeleteMailingView, \
    DetailMailingView, CreateClientView, ListClientView, DeleteClientView, MailingLogListView, DeleteMailingLogView, \
    DetailMailingLogView, DetailClientView, UpdateClientView, CreateMessageView, ListMessageView, UpdateMessageView, \
    DeleteMessageView, DetailMessageView

app_name = 'mailings'

urlpatterns = [
    path('mailing/create', CreateMailingView.as_view(), name='create_mailing'),
    path('mailing/list', ListMailingView.as_view(), name='list_mailing'),
    path('mailing/update/<int:pk>/', UpdateMailingView.as_view(), name='update_mailing'),
    path('mailing/delete/<int:pk>/', DeleteMailingView.as_view(), name='delete_mailing'),
    path('mailing/detail/<int:pk>/', DetailMailingView.as_view(), name='detail_mailing'),

    path('client/create/', CreateClientView.as_view(), name='create_client'),
    path('client/list/', ListClientView.as_view(), name='list_client'),
    path('client/update/<int:pk>/', UpdateClientView.as_view(), name='update_client'),
    path('client/detail/<int:pk>/', DetailClientView.as_view(), name='detail_client'),
    path('client/delete/<int:pk>/', DeleteClientView.as_view(), name='delete_client'),

    path('message/create/', CreateMessageView.as_view(), name='create_message'),
    path('message/list/', ListMessageView.as_view(), name='list_message'),
    path('message/update/<int:pk>/', UpdateMessageView.as_view(), name='update_message'),
    path('message/delete/<int:pk>/', DeleteMessageView.as_view(), name='delete_message'),
    path('message/detail/<int:pk>/', DetailMessageView.as_view(), name='detail_message'),

    path('logs/', MailingLogListView.as_view(), name='mailing_logs_list'),
    path('logs/detail/<int:pk>/', DetailMailingLogView.as_view(), name='mailing_log_detail'),
    path('log/delete/<int:pk>/', DeleteMailingLogView.as_view(), name='delete_mailing_log'),
]