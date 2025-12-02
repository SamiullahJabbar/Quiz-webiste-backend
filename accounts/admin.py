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

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id','email','first_name','last_name','education','is_active','is_staff')
#     actions = ['approve_users','reject_users']

#     def approve_users(self, request, queryset):
#         for user in queryset:
#             user.is_active = True
#             user.save()
#             send_approval_email(user)
#     approve_users.short_description = "Approve selected users"

#     def reject_users(self, request, queryset):
#         for user in queryset:
#             send_rejection_email(user)
#             user.delete()
#     reject_users.short_description = "Reject selected users"



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('id', 'email', 'first_name', 'last_name', 'education', 'is_active', 'is_staff', 'otp_verified')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'otp_code', 'otp_verified')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'education', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'education', 'date_of_birth', 'password1', 'password2'),
        }),
    )

    actions = ['approve_users', 'reject_users']

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
