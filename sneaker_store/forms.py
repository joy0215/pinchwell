from django import forms
from products.models import UserProfile ,Employee ,Inventory ,SignupProfile, Member
from django.contrib.auth.forms import User ,UserCreationForm
import datetime


class SignupForm(forms.ModelForm):
    member_id = forms.CharField(label='會員編號', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Member
        fields = ['member_id', 'username', 'password', 'email', 'phone_number', 'birthdate', 'gender', 'bio']
        widgets = {
            'password': forms.PasswordInput(),
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        today = datetime.date.today()
        time_now = datetime.datetime.now().strftime('%H%M%S')
        date_str = today.strftime('%Y%m%d')
        self.fields['member_id'].initial = f'VIP{date_str}{time_now}'


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


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

class InventoryUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        super(InventoryUpdateForm, self).__init__(*args, **kwargs)
        
        # 根據 product_id 從 Inventory 中獲取庫存尺寸
        inventory_sizes = Inventory.objects.filter(product_id=product_id).values_list('size', flat=True)
        
        # 為每個尺寸創建一個表單字段
        for size in inventory_sizes:
            self.fields[f'size_{size}'] = forms.IntegerField(label=size, initial=0)


class PasswordForm(forms.Form):
    password = forms.CharField(label='密碼', widget=forms.PasswordInput)

class EditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'profile_picture', 'employee_id']

from django import forms
from django.contrib.auth.models import User

class SignupUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class SignupProfileForm(forms.ModelForm):
    class Meta:
        model = SignupProfile
        fields = ('location', 'birthdate', 'bio','gender')

