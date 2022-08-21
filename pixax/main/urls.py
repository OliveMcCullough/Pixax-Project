from django.urls import path
from .views import AlbumView, RootRedirectView, MyAlbumsView, UploadPicturesView, UnsortedPicturesView, AlbumDeleteView, AlbumEditNameView, AlbumRateSortView

app_name = "main"

urlpatterns = [
    path('', RootRedirectView.as_view(), name='root'),
    path('albums/', MyAlbumsView.as_view(), name='albums'),
    path('albums/<int:pk>/', AlbumView.as_view(), name='album'),
    path('albums/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
    path('albums/<int:pk>/edit/', AlbumEditNameView.as_view(), name="album_edit_name"),
    path('albums/<int:pk>/organise/setup/', AlbumRateSortView.as_view(), name="album_organise"),
    path('upload/', UploadPicturesView.as_view(), name="upload"),
    path('albums/unsorted/', UnsortedPicturesView.as_view(), name="unsorted"),
]