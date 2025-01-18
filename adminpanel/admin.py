from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    Profile,
    Job,
    Application,
    Notification,
    SavedJob,
    SavedFilter,
    ActivityLog,NotificationPreference,CandidateDocument)

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('email',)

# Profile Admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'mobile', 'company')
    search_fields = ('name', 'email', 'mobile', 'company')
    list_filter = ('company',)
    ordering = ('user',)

# Job Admin
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'job_location', 'job_region', 'job_type', 'posted_by', 'posted_at')
    search_fields = ('job_title', 'job_location', 'company_name')
    list_filter = ('job_region', 'job_type', 'posted_at')
    ordering = ('-posted_at',)

# Application Admin
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at')
    search_fields = ('job__job_title', 'applicant__username', 'status')
    list_filter = ('status', 'applied_at')
    ordering = ('-applied_at',)

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)

# Saved Job Admin
@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    search_fields = ('user__username', 'job__job_title')
    ordering = ('-saved_at',)

# Saved Filter Admin
@admin.register(SavedFilter)
class SavedFilterAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('user__username', 'name')
    ordering = ('user',)

# Activity Log Admin
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_at')
    search_fields = ('user__username', 'action')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

# Register the Custom User Admin
admin.site.register(CustomUser, CustomUserAdmin)



@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_alerts', 'new_job_alerts', 'application_status_updates')
    search_fields = ('user__username', 'user__email')
    list_filter = ('email_alerts', 'new_job_alerts', 'application_status_updates')
    ordering = ('user',)

    def has_add_permission(self, request):
        """
        Prevent adding NotificationPreference directly from admin as it should
        be auto-created when a user is registered.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting NotificationPreference directly from admin.
        """
        return False



@admin.register(CandidateDocument)
class CandidateDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'resume', 'portfolio', 'certifications')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active',)
    readonly_fields = ('user',)

    def get_readonly_fields(self, request, obj=None):
        # Allow editing the user field only when creating a new instance
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields
