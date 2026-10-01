from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'country')


class CustomAuthenticationForm(AuthenticationForm):
    pass