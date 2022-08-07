from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegistrationForm


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(*args, **kwargs)
        else:
            return super().dispatch(*args, **kwargs)