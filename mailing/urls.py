from django.urls import path
from .views import RecipientCreate, RecipientDetailView, RecipientUpdateView, RecipientDelete, RecipientList, MessageCreate, MessageDetailView, MessageUpdateView, MessageList, MessageDelete, MessengerUpdateView, MessengerDelete, MessengerCreate, MessengerList, MessengerDetailView
app_name = 'mailing'

urlpatterns = [
    path('recipients/', RecipientList.as_view(), name='recipient_list'),
    path('recipient/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/new/', RecipientCreate.as_view(), name='recipient_create'),
    path('recipient/<int:pk>/edit/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/<int:pk>/delete/', RecipientDelete.as_view(), name='recipient_delete'),
    path('messages/', MessageList.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/new/', MessageCreate.as_view(), name='message_create'),
    path('message/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDelete.as_view(), name='message_delete'),
    path('messenger/', MessengerList.as_view(), name='list_messenger'),
    path('messenger/<int:pk>/', MessengerDetailView.as_view(), name='messenger_detail'),
    path('messenger/new/', MessengerCreate.as_view(), name='messenger_create'),
    path('messenger/<int:pk>/edit/', MessengerUpdateView.as_view(), name='messenger_update'),
    path('messenger/<int:pk>/delete/', MessengerDelete.as_view(), name='messenger_delete'),

]