from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import AuthenticationKey
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    authentication_key = forms.CharField(label="인증키")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "authentication_key")

    def clean_authentication_key(self):
        authentication_key = self.cleaned_data.get('authentication_key')
        if not AuthenticationKey.objects.filter(key=authentication_key, is_valid=True).exists():
            raise ValidationError("유효하지 않은 인증키입니다.")
        return authentication_key
