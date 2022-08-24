from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegistrationForm
from .models import User


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main:root')
        else:
            return super().dispatch(*args, **kwargs)


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main:root')
        else:
            return super().dispatch(*args, **kwargs)

    def form_invalid(self, form):
        form_invalid = super().form_invalid(form)
        user_name = form.cleaned_data.get("username")
        try:
            user = User.objects.filter(username=user_name).first()
            if not user.is_active:
                form.add_error("username", """You account is not active. It may still be awaiting admin approval.""")
                return super().form_invalid(form)
        except:
            return form_invalid

    def get_success_url(self, *args, **kwargs):
        return super().get_success_url(*args, **kwargs)