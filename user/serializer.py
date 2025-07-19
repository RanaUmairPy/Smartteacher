from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import send_otp_email
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'name', 'roll_number', 'age', 'profile_picture')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        send_otp_email(user)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
       def validate(self, attrs):
        
        data = super().validate(attrs)
        
        # Check if user is verified
        if not self.user.is_verified:
            raise serializers.ValidationError({"error": "Email is not verified. Please verify your email before logging in."})
        
        
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "name": self.user.name,
            "email": self.user.email,
            "roll_number": self.user.roll_number,
            "age": self.user.age,
            "profile_picture": self.user.profile_picture.url if self.user.profile_picture else None,
            "is_teacher": self.user.is_teacher,
        }
        return data

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        try:
            user = User.objects.get(email=email)
            if user.email_otp != otp:
                raise serializers.ValidationError({"error": "Invalid OTP"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User not found"})
        return attrs