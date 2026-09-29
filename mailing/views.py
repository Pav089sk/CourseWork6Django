from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View, TemplateView
from .models import Recipient, Message, Messenger, Attempt
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from mailing.forms import MessengerForm

class RecipientCreate(CreateView):
    model = Recipient
    fields = ['email', 'first_name', 'last_name', 'middle_name', 'comment']
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecipientList(ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)

class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'mailing/recipient_detail.html'
    context_object_name = 'recipient'

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)

class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ['email', 'first_name', 'last_name', 'middle_name', 'comment']
    template_name = 'mailing/recipient_form.html'

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('mailing:recipient_detail', kwargs={'pk': self.object.pk})

class RecipientDelete(DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)


class MessageCreate(CreateView):
    model = Message
    fields = ['theme', 'content']
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MessageList(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

class MessageUpdateView(UpdateView):
    model = Message
    fields = ['theme', 'content']
    template_name = 'mailing/message_form.html'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})

class MessageDelete(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessengerCreate(CreateView):
    model = Messenger
    form_class = MessengerForm
    template_name = 'mailing/messenger_form.html'
    success_url = reverse_lazy('mailing:list_messenger')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MessengerList(ListView):
    model = Messenger
    template_name = 'mailing/messenger_list.html'
    context_object_name = 'messengers'

    def get_queryset(self):
        return Messenger.objects.filter(user=self.request.user)

class MessengerDetailView(DetailView):
    model = Messenger
    template_name = 'mailing/messenger_detail.html'
    context_object_name = 'messenger'

    def get_queryset(self):
        return Messenger.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

class MessengerUpdateView(UpdateView):
    model = Messenger
    form_class = MessengerForm
    template_name = 'mailing/messenger_form.html'

    def get_queryset(self):
        return Messenger.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('mailing:messenger_detail', kwargs={'pk': self.object.pk})

class MessengerDelete(DeleteView):
    model = Messenger
    template_name = 'mailing/messenger_confirm_delete.html'
    success_url = reverse_lazy('mailing:list_messenger')

    def get_queryset(self):
        return Messenger.objects.filter(user=self.request.user)

class AttemptDetailView(DetailView):
    model = Attempt
    template_name = 'mailing/attempt_detail.html'
    context_object_name = 'attempt'

class SendMailView(View):
    def post(self,request, *args, **kwargs ):
        messenger = get_object_or_404(Messenger, pk=self.kwargs['pk'], user=self.request.user)
        now = timezone.now()
        if not (messenger.start_time <= now <= messenger.end_time):
            messages.error(request, 'Ошибка: отправка возможна только между start_time и end_time.')
            return redirect('mailing:messenger_detail', pk=messenger.pk)
        attempts = []

        for recipient in messenger.recipients.all():
            try:
                send_mail(
                    messenger.message.theme,
                    messenger.message.content,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient.email]
                )
                attempts.append(Attempt(
                    status=Attempt.SUCCESS,
                    server_response='Отправлено',
                    mailing=messenger,
                    recipient=recipient
                ))
            except Exception as e:
                attempts.append(Attempt(
                    status=Attempt.FAIL,
                    server_response=str(e),
                    mailing=messenger,
                    recipient=recipient
                ))
        Attempt.objects.bulk_create(attempts)
        messages.success(request, f"Рассылка №{messenger.pk} запущена. Письма отправлены.")
        return redirect('mailing:messenger_detail', pk=messenger.pk)

class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['total_mailings'] = Messenger.objects.count()
        context['active_mailings'] = Messenger.objects.filter(
            start_time__lte=now,
            end_time__gte=now
        ).count()
        context['unique_recipients'] = Recipient.objects.count()
        return context