from django.urls import path
from .views import RegisterView,MyTokenObtainPairView,VerifyOTPView,StorePlayerIdView, ClearPlayerIdView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('store-player-id/', StorePlayerIdView.as_view(), name='store-player-id'),
    path('clear-player-id/', ClearPlayerIdView.as_view(), name='clear-player-id'),
]
