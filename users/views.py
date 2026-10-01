from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from users.forms import CustomUserCreationForm
from django.views.generic import CreateView
from users.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from users.models import CustomUser
import random

class CustomLoginView(LoginView):
    template_name = 'users/login.html'


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        base_username = user.email.split('@')[0]
        username = base_username
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{random.randint(100, 999)}"
        user.username = username
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        domain = get_current_site(self.request).domain
        activation_link = f"http://{domain}/users/activate/{uid}/{token}/"
        subject = "Подтвердите ваш email"
        message = f"Перейдите по ссылке, чтобы подтвердить регистрацию:\n{activation_link}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)
        messages.success(self.request, 'Мы отправили письмо для подтверждения email.')
        return redirect('users:login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш аккаунт активирован.')
        return redirect('users:login')
    else:
        return render(request, 'users/activation_invalid.html')


