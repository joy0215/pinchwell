from django import forms
from products.models import UserProfile
from django.contrib.auth.forms import UserCreationForm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthdate', 'phone']  # 只包含 UserProfile 模型中的字段
