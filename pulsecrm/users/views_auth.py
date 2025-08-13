from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .authentication import EmailTokenObtainPairSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Ensure a professional, consistent payload
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            return Response({
                "access": data.get("access"),
                "refresh": data.get("refresh"),
                "role": data.get("role"),
                "email": data.get("email"),
                "message": data.get("message", "Login successful"),
            }, status=status.HTTP_200_OK)
        return response