from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False  # ✅ inactive until admin approves
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    EDUCATION_CHOICES = (
        ('school', 'School'),
        ('college', 'College'),
        ('university', 'University'),
    )
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    otp_code = models.CharField(max_length=6, null=True, blank=True)  # ✅ store OTP
    otp_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.education})"
