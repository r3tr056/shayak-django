from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import User, LoginAttempt, Feature, UserSettings

class UserAdmin(BaseUserAdmin):
    """ Admin configuration for the User model """
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'user_type', 'email_verified', 'phone_verified', 'location']
    list_filter = ['user_type', 'is_active', 'email_verified', 'phone_verified']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'date_of_birth', 'phone_number', 'location')}),
        (_('Permissions'), {'fields': ('is_active', 'user_type', 'email_verified', 'phone_verified')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'user_type', 'email_verified', 'phone_verified', 'is_active'),
        }),
    )

admin.site.register(User, UserAdmin)

class LoginAttemptAdmin(admin.ModelAdmin):
    """ Admin configuration for LoginAttempt model """
    list_display = ['user', 'timestamp', 'location', 'device_id']
    search_fields = ['user__email', 'location', 'device_id']
    list_filter = ['timestamp', 'location']

admin.site.register(LoginAttempt, LoginAttemptAdmin)

class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Feature, FeatureAdmin)

class UserSettingsAdmin(admin.ModelAdmin):
    """ Admin configuration for UserSettings model """
    list_display = ['user', 'ai_creativity_level']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    filter_horizontal = ('allowed_features',)

admin.site.register(UserSettings, UserSettingsAdmin)