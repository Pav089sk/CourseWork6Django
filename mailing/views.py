from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Recipient, Message, Messenger
from django.urls import reverse_lazy

class RecipientCreate(CreateView):
    model = Recipient
    fields = ['email', 'first_name', 'last_name', 'middle_name', 'comment']
    template_name = 'recipient_form.html'
    success_url = reverse_lazy('recipient_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecipientList(ListView):
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)

class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'recipient_detail.html'
    context_object_name = 'recipient'

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)

class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ['email', 'first_name', 'last_name', 'middle_name', 'comment']
    template_name = 'recipient_form.html'

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('recipient_detail', kwargs={'pk': self.object.pk})

class RecipientDelete(DeleteView):
    model = Recipient
    template_name = 'recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient_list')

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)


class MessageCreate(CreateView):
    model = Message
    fields = ['theme', 'content']
    template_name = 'message_form.html'
    success_url = reverse_lazy('message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MessageList(ListView):
    model = Message
    template_name = 'message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

class MessageDetailView(DetailView):
    model = Message
    template_name = 'message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

class MessageUpdateView(UpdateView):
    model = Message
    fields = ['theme', 'content']
    template_name = 'message_form.html'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('message_detail', kwargs={'pk': self.object.pk})

class MessageDelete(DeleteView):
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('message_list')

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessengerCreate(CreateView):
    model = Messenger
    fields = ['start_time', 'end_time', 'message', 'recipients']
    template_name = 'messenger_form.html'
    success_url = reverse_lazy('list_messenger')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MessengerList(ListView):
    model = Messenger
    template_name = 'messenger_list.html'
    context_object_name = 'messengers'

    def get_queryset(self):
        return Messenger.objects.filter(user=self.request.user)

class MessengerDetailView(DetailView):
    model = Messenger
    template_name = 'messenger_detail.html'
    context_object_name = 'messenger'

    def get_queryset(self):
        return Messenger.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj

class MessengerUpdateView(UpdateView):
    model = Messenger
    fields = ['start_time', 'end_time', 'message', 'recipients']
    template_name = 'messenger_form.html'

    def get_queryset(self):
        return Messenger.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('messenger_detail', kwargs={'pk': self.object.pk})

class MessengerDelete(DeleteView):
    model = Messenger
    template_name = 'messenger_confirm_delete.html'
    success_url = reverse_lazy('list_messenger')

    def get_queryset(self):
        return Messenger.objects.filter(user=self.request.user)