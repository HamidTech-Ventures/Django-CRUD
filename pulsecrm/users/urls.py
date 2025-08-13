from django.urls import path
from .views import MeView, RegisterView

urlpatterns = [
    path("users/me/", MeView.as_view(), name="me"),
    path("users/register/", RegisterView.as_view(), name="register"),
]