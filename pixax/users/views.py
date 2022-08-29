from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, UpdateView


from .forms import UserRegistrationForm, ProfileUsernameEditForm, ProfilePicEditForm
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
                form.add_error("username", """Your account is not active. It may still be awaiting admin approval.""")
                return super().form_invalid(form)
        except:
            return form_invalid

    def get_success_url(self, *args, **kwargs):
        return super().get_success_url(*args, **kwargs)


class ProfileView(TemplateView):
    template_name = "profile.html"


class ProfileUsernameEditView(UpdateView):
    template_name = "profile_username_edit.html"
    model = User
    form_class = ProfileUsernameEditForm
    success_url = reverse_lazy("users:profile")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        return self.request.user


class ProfilePicEditView(UpdateView):
    template_name = "profile_pic_edit.html"
    model = User
    form_class = ProfilePicEditForm
    success_url = reverse_lazy("users:profile")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        return self.request.user