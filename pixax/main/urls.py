from django.urls import path
from .views import AlbumDetailView, RootRedirectView, MyAlbumsView, UploadPicturesView

app_name = "main"

urlpatterns = [
    path('', RootRedirectView.as_view(), name='root'),
    path('albums/', MyAlbumsView.as_view(), name='albums'),
    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album'),
    path('upload/', UploadPicturesView.as_view(), name="upload"),
]