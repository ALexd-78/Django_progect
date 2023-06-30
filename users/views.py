from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from users.forms import UserForm, UserRegisterForm
from users.models import User


class RegisterView(generic.CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались. Проверьте почту для активации!'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.token = default_token_generator.make_token(new_user)
        activation_url = reverse_lazy(
            'users:confirm_email', kwargs={'token': new_user.token}
        )

        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения регистрации перейдите по ссылке: http://localhost:8000/{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        new_user.save()
        return redirect('users:email_confirmation_sent')

class UserConfirmEmailView(generic.View):
    def get(self, request, token):
        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            return redirect('users:email_confirmation_failed')

        user.is_active = True
        user.token = None
        user.save()
        return redirect('users:login')

class EmailConfirmationSentView(generic.TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmView(generic.TemplateView):
    template_name = 'users/email_verified.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context

class EmailConfirmationFailedView(generic.TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context

class ProfileUpdateView(generic.UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.email}'
        return context
