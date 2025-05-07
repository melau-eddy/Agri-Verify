from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = ('user', 'truncated_message', 'truncated_response', 
                   'is_agriculture_related', 'created_at')
    
    # Make fields clickable for editing
    list_display_links = ('user', 'truncated_message')
    
    # Add filters
    list_filter = ('is_agriculture_related', 'created_at', 'user')
    
    # Add search functionality
    search_fields = ('message', 'response', 'user__username')
    
    # Fields to display in edit view
    fieldsets = (
        (None, {
            'fields': ('user', 'created_at')
        }),
        ('Message Content', {
            'fields': ('message', 'response', 'is_agriculture_related'),
            'classes': ('wide',),
        }),
    )
    
    # Make created_at read-only
    readonly_fields = ('created_at',)
    
    # Custom methods for truncated display
    def truncated_message(self, obj):
        return obj.message[:75] + '...' if len(obj.message) > 75 else obj.message
    truncated_message.short_description = 'Message'
    
    def truncated_response(self, obj):
        return obj.response[:75] + '...' if len(obj.response) > 75 else obj.response
    truncated_response.short_description = 'Response'
    
    # Order by most recent first by default
    ordering = ('-created_at',)