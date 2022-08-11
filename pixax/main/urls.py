from django.urls import path
from .views import RootRedirectView

app_name = "main"

urlpatterns = [
    path('', RootRedirectView.as_view(), name='home'),
]