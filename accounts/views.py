import random
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import User
from .serializers import RegisterSerializer

def send_otp_email(user, otp):
    subject = "Verify your email"
    message = render_to_string("email/otp_email.html", {
        "first_name": user.first_name,
        "otp": otp,
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"
    email.send()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        otp = str(random.randint(100000,999999))
        user.otp_code = otp
        user.is_active = False   # ✅ inactive until admin approves
        user.save()

        send_otp_email(user, otp)

        return Response({
            "id": user.id,
            "email": user.email,
            "message": "Account created successfully. OTP has been sent to your email."
        })

class VerifyOTPView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message":"User not found"}, status=404)

        if user.otp_code == otp:
            user.otp_verified = True
            user.save()
            return Response({
                "message": "OTP verified. Your request has been sent to admin. You will receive an email soon."
            })
        return Response({"message":"Invalid OTP"}, status=400)

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

