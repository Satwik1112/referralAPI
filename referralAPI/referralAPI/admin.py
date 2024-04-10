from django.contrib import admin
from .models import User, LoginHistory


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["userID", "name", "email", "password", "referral_code", "referral_score", "registered_time"]


@admin.register(LoginHistory)
class UserAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "last_login_time"]
