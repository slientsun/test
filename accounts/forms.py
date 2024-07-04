from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django import forms


# 创建用户注册表单
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=128, required=True, widget=forms.EmailInput())

    class Meta:
        model = User  # 继承User
        fields = ('username', 'email', 'password1', 'password2')
