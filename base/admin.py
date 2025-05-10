from django.contrib import admin
from .models import ChatMessage
from .models import Webinar

@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ('title', 'scheduled_time', 'is_active')
    list_filter = ('is_active', 'scheduled_time')
    search_fields = ('title', 'description')
    date_hierarchy = 'scheduled_time'

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


from django.contrib import admin
from .models import GovernmentApproval, EducationalVideo, VerifiedProduct

@admin.register(GovernmentApproval)
class GovernmentApprovalAdmin(admin.ModelAdmin):
    list_display = ('approval_id', 'approving_body', 'status', 'approval_date', 'risk_level')
    list_filter = ('status', 'approving_body')
    search_fields = ('approval_id', 'approving_body')
    readonly_fields = ('approval_id',)

@admin.register(EducationalVideo)
class EducationalVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'duration', 'related_approval')
    list_filter = ('source', 'related_approval__approving_body')
    search_fields = ('title', 'description')

@admin.register(VerifiedProduct)
class VerifiedProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'product_type', 'approval_status')
    list_filter = ('product_type', 'approval__status')
    search_fields = ('name', 'manufacturer', 'approval__approval_id')
    
    def approval_status(self, obj):
        return obj.approval.get_status_display()
    approval_status.short_description = 'Approval Status'