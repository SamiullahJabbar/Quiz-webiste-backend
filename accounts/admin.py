from django.contrib import admin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import User

def send_approval_email(user):
    subject = "Account Approved"
    message = render_to_string("email/approval_email.html", {
        "first_name": user.first_name,
        "login_link": "http://127.0.0.1:8000/login/"
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"
    email.send()

def send_rejection_email(user):
    subject = "Account Rejected"
    message = render_to_string("email/rejection_email.html", {
        "first_name": user.first_name
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"
    email.send()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','first_name','last_name','education','is_active','is_staff')
    actions = ['approve_users','reject_users']

    def approve_users(self, request, queryset):
        for user in queryset:
            user.is_active = True
            user.save()
            send_approval_email(user)
    approve_users.short_description = "Approve selected users"

    def reject_users(self, request, queryset):
        for user in queryset:
            send_rejection_email(user)
            user.delete()
    reject_users.short_description = "Reject selected users"
