from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm

User = get_user_model()

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Изменение пароля'}

class UserPasswordReset(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    extra_context = {'title': 'Восстановление пароля'}

class UserPasswordResetDone(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    extra_context = {'title': 'Письмо отправлено'}

class UserPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    extra_context = {'title': 'Новый пароль'}

class UserPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    extra_context = {'title': 'Пароль изменён'}