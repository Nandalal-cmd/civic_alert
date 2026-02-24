from django.contrib import admin
from .models import Complaint, Notification

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    # What columns show up in the list
    list_display = ('category', 'citizen', 'status', 'created_at')
    # Filter sidebar for quick navigation
    list_filter = ('status', 'category')
    # Search bar for descriptions or usernames
    search_fields = ('description', 'citizen__username')
    # Allow editing status directly from the list view
    list_editable = ('status',)

    def save_model(self, request, obj, form, change):
        # Save the actual complaint first
        super().save_model(request, obj, form, change)
        
        # If the status was updated (not a new complaint)
        if change:
            Notification.objects.create(
                user=obj.citizen,
                complaint=obj,
                message=f"Update: Your {obj.category} report status is now '{obj.status}'."
            )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'complaint', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    readonly_fields = ('created_at',)