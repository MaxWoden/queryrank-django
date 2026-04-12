from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин или Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Такой Email уже зарегистрирован')
        return email

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'date_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))