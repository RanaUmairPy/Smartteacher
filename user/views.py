from rest_framework import generics, permissions
from .serializer import RegisterSerializer,MyTokenObtainPairSerializer,VerifyOTPSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser  # Assuming you have a CustomUser model defined
from .utils import send_otp_email  # Assuming you have a utility function to send OTP emails

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class VerifyOTPView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyOTPSerializer  # Added serializer class

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate input
        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            user.is_verified = True
            user.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)