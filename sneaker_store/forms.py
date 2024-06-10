from django import forms
from products.models import UserProfile ,Employee ,Inventory ,SignupProfile, Member,Feedback
from django.contrib.auth.forms import User ,UserCreationForm
import datetime


class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 0}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['member', 'product', 'comment', 'product_satisfaction', 'brand_satisfaction', 'delivery_satisfaction']
        labels = {
            'member': '客戶編號',
            'product': '商品名稱',
            'comment': '留言',
            'product_satisfaction': '商品滿意度',
            'brand_satisfaction': '品牌滿意度',
            'delivery_satisfaction': '宅配滿意度',
        }
    
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['member'].queryset = self.fields['member'].queryset.order_by('member_id')
        self.fields['member'].label_from_instance = lambda obj: obj.member_id

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


class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['size', 'quantity']  # 更新字段名稱
        labels = {
            'size': '尺寸',
            'quantity': '庫存量',  # 更新字段名稱
        }
        widgets = {
            'size': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['size', 'quantity']  # 更新字段名稱
        labels = {
            'size': '尺寸',
            'quantity': '庫存量',
        }
        widgets = {
            'size': forms.TextInput(attrs={'readonly': 'readonly'}),
        }