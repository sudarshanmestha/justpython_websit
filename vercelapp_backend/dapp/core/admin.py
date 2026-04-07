# core/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # This displays the fields from your UserSerializer in the admin list
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
    # This adds a search bar to find users easily
    search_fields = ('username', 'email', 'first_name', 'last_name')

    