from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views_auth import EmailTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth endpoints
    path("api/auth/token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # App endpoints
    path("api/", include("users.urls")),
    path("api/", include("employees.urls")),
    path("api/", include("clients.urls")),
    path("api/", include("projects.urls")),
    path("api/", include("chat.urls")),
]