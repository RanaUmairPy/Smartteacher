from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True)  # lowercase preferred for consistency
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    email_otp = models.CharField(max_length=6, blank=True, null=True)  # Increased to 6 digits for better security
    is_verified = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False,null=True,blank=True)  # True if the user is a teacher, False if a student
    onesignal_player_id = models.CharField(max_length=100, blank=True, null=True)
    #otp_created_at = models.DateTimeField(auto_now=True)  # Track when OTP was generated

    def __str__(self):
        return f"{self.username} ({self.email})"

    def generate_email_otp(self):
        
        return str(secrets.randbelow(900000) + 100000)  # Ensures 100000–999999 range

    def save(self, *args, **kwargs):
        if not self.email_otp:
            self.email_otp = self.generate_email_otp()
        super().save(*args, **kwargs)


