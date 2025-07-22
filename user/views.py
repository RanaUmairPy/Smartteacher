from rest_framework import generics, permissions
from .serializer import RegisterSerializer,MyTokenObtainPairSerializer,VerifyOTPSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser  # Assuming you have a CustomUser model defined
from .utils import send_otp_email,send_success_email  # Assuming you have a utility function to send OTP emails
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model

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
            send_success_email(user.email, user.username)
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        



User = get_user_model()

class StorePlayerIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        player_id = request.data.get('player_id')
        if not user_id or not player_id:
            return Response({"error": "user_id and player_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            if user != request.user:
                return Response({"error": "Unauthorized to update this user's player ID"}, status=status.HTTP_403_FORBIDDEN)
            user.onesignal_player_id = player_id
            user.save()
            return Response({"message": "Player ID stored successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ClearPlayerIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.onesignal_player_id = None
            user.save()
            return Response({"message": "Player ID cleared successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error clearing player ID: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
