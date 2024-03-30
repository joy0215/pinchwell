from django import forms
from products.models import UserProfile ,Employee
from django.contrib.auth.forms import User ,UserCreationForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthdate', 'phone']

class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

class EmployeePasswordForm(forms.Form):
    password = forms.CharField(label='密碼', widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.initial['username']
        user = User.objects.get(username=username)

        if not user.check_password(password):
            raise forms.ValidationError('無效的密碼')
        
        return password

class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'profile_picture', 'employee_id']  # 指定要在表單中顯示的欄位


    def __init__(self, *args, **kwargs):
        super(EmployeeEditForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].required = False



class PasswordForm(forms.Form):
    password = forms.CharField(label='密碼', widget=forms.PasswordInput)

class EditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'profile_picture', 'employee_id']

