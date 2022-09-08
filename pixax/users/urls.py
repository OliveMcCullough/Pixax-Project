from django.urls import path
from .views import FriendAdd, FriendAddDone, FriendLinkConfirm, FriendList, FriendRequestAccept, FriendRequestList, FriendRequestReject, ProfilePicEditView, RegisterView, LoginView, ProfileView, ProfileUsernameEditView, UnfriendConfirmation

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/username/edit/", ProfileUsernameEditView.as_view(), name="profile_username_edit"),
    path("profile/picture/edit/", ProfilePicEditView.as_view(), name="profile_pic_edit"),
    path("friends/", FriendList.as_view(), name="friends"),
    path("friends/<int:user_id>/unfriend/", UnfriendConfirmation.as_view(), name="unfriend"),
    path("friends/requests/", FriendRequestList.as_view(), name="friend_requests"),
    path("friends/requests/<int:user_id>/reject/", FriendRequestReject.as_view(), name="friend_request_reject"),
    path("friends/requests/<int:user_id>/accept/", FriendRequestAccept.as_view(), name="friend_request_accept"),
    path("friends/add/", FriendAdd.as_view(), name="friend_add"),
    path("friends/add/done/", FriendAddDone.as_view(), name="friend_add_done"),
    path("friends/add/<uuid:link_id>/", FriendLinkConfirm.as_view(), name="friend_add_link_confirm")
]