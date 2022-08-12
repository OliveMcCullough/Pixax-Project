from django.urls import path
from .views import RootRedirectView, MyAlbumsView

app_name = "main"

urlpatterns = [
    path('', RootRedirectView.as_view(), name='root'),
    path('albums/', MyAlbumsView.as_view(), name='albums'),
]