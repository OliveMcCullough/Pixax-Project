from django.urls import path
from .views import AlbumSharedView, AlbumView, FriendSharedAlbumsView, PictureDeleteView, RootRedirectView, MyAlbumsView, UploadPicturesView, UnsortedPicturesView, AlbumDeleteView, AlbumEditNameView, AlbumRateSortIntroView, AboutView, UnsortedRateSortIntroView, UnsortedRateSortActiveView, AlbumRateSortActiveView, PictureEditView, SetAlbumShareSettings, AlbumPublicView

app_name = "main"

urlpatterns = [
    path('', RootRedirectView.as_view(), name='root'),
    path('albums/', MyAlbumsView.as_view(), name='albums'),
    path('albums/<int:pk>/', AlbumView.as_view(), name='album'),
    path('shared/users/<int:pk>/', FriendSharedAlbumsView.as_view(), name='friend_shared_album_list'),
    path('shared/albums/<int:pk>/', AlbumSharedView.as_view(), name='album_shared'),
    path('public/albums/<int:pk>/', AlbumPublicView.as_view(), name='album_public'),
    path('albums/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
    path('albums/<int:pk>/edit/', AlbumEditNameView.as_view(), name="album_edit_name"),
    path('albums/<int:pk>/share-settings/', SetAlbumShareSettings.as_view(), name="album_share_settings_set"),
    path('albums/<int:pk>/organise/setup/', AlbumRateSortIntroView.as_view(), name="album_organise"),
    path('albums/<int:pk>/organise/', AlbumRateSortActiveView.as_view(), name="album_organise_active"),
    path('upload/', UploadPicturesView.as_view(), name="upload"),
    path('albums/unsorted/', UnsortedPicturesView.as_view(), name="unsorted"),
    path('albums/unsorted/organise/setup/', UnsortedRateSortIntroView.as_view(), name="unsorted_organise"),
    path('albums/unsorted/organise/', UnsortedRateSortActiveView.as_view(), name="unsorted_organise_active"),
    path('albums/<int:album_id>/pictures/<int:pk>/edit/', PictureEditView.as_view(), name="pic_edit"),
    path('pictures/<int:pk>/edit/', PictureEditView.as_view(), name="pic_edit"),
    path('albums/<int:album_id>/pictures/<int:pk>/delete/', PictureDeleteView.as_view(), name="pic_delete"),
    path('pictures/<int:pk>/delete/', PictureDeleteView.as_view(), name="pic_delete"),
    path('about/', AboutView.as_view(), name="about"),
]