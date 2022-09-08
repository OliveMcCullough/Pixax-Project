from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, FormView, ListView, RedirectView, TemplateView, UpdateView



from .forms import FriendAddForm, FriendLinkConfirmForm, UnfriendConfirmationForm, UserRegistrationForm, ProfileUsernameEditForm, ProfilePicEditForm
from .models import Friendship, User


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
            pass
        return form_invalid


class ProfileView(TemplateView):
    template_name = "profile.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


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


class FriendAdd(FormView):
    template_name = "friend_add.html"
    form_class = FriendAddForm
    success_url = reverse_lazy("users:friend_add_done")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get("friend_email").strip()
        user = self.request.user
        try:
            other_user = User.objects.get(email__iexact=email)
            Friendship.make_friend_request(user, other_user)
        except:
            pass
        return super().form_valid(form)


class FriendAddDone(TemplateView):
    template_name = "friend_add_done.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        

class FriendList(ListView):
    template_name = "friends_list.html"
    model = User
    context_object_name = "friends"
    paginate_by = 2
    ordering = ["username"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        friends = user.friends.values_list("from_user", flat=True)
        qs = qs.filter(id__in=friends)
        return qs


class FriendRequestList(ListView):
    template_name = "friend_requests.html"
    model = User
    context_object_name = "requests"
    paginate_by = 2
    ordering = ["username"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        requests = user.friendship_requests_received.values_list("from_user", flat=True)
        qs = qs.filter(id__in=requests)
        return qs


class FriendLinkConfirm(FormView):
    template_name = "friend_link_confirm.html"
    form_class = FriendLinkConfirmForm
    success_url = reverse_lazy("users:friends")
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        link_id = self.kwargs['link_id']
        friends_id = Friendship.list_friends(user).values_list("id", flat=True)
        other_user = User.objects.filter(unique_link_id=link_id).exclude(id=user.id).exclude(id__in=friends_id)
        if other_user.count() != 1:
            raise Http404
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        user = self.request.user
        link_id = self.kwargs['link_id']
        other_user = User.objects.filter(unique_link_id=link_id).exclude(id=user.id).first()
        Friendship.create_friendship(user, other_user)
        return form_valid


class FriendLinkConfirmDone(DetailView):
    template_name = "friend_link_confirm_done.html"
    model = User
    context_object_name = "friend"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class FriendRequestReject(RedirectView):
    permanent = False
    query_string = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        user1 = self.request.user
        user2_id = self.kwargs["user_id"]
        user2 = User.objects.get(id=user2_id)
        if Friendship.check_friend_request_exists(from_user=user2, to_user=user1):
            Friendship.reject_friend_request(user2, user1)
        else:
            raise Http404
        return reverse_lazy("users:friends")


class FriendRequestAccept(RedirectView):
    permanent = False
    query_string = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        user1 = self.request.user
        user2_id = self.kwargs["user_id"]
        user2 = User.objects.get(id=user2_id)
        if Friendship.check_friend_request_exists(from_user=user2, to_user=user1):
            Friendship.create_friendship(user1, user2)
        else:
            raise Http404
        return reverse_lazy("users:friends")


class UnfriendConfirmation(FormView):
    template_name = "unfriend_confirm.html"
    form_class = UnfriendConfirmationForm
    success_url = reverse_lazy("users:friends")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        friend_id = self.kwargs["user_id"]
        friend = User.objects.get(id=friend_id)
        if Friendship.check_friendship(user, friend):
            return super().dispatch(*args, **kwargs)
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_id = self.kwargs["user_id"]
        friend = User.objects.get(id=friend_id)
        context["friend"] = friend
        return context

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        user = self.request.user
        friend_id = self.kwargs["user_id"]
        friend = User.objects.get(id=friend_id)
        Friendship.remove_friendship(user, friend)
        return form_valid