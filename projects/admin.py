from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description', 'owner__email', 'owner__name')
    readonly_fields = ('created_at',)
    filter_horizontal = ('participants',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'owner', 'status')
        }),
        ('Дополнительно', {
            'fields': ('github_url', 'created_at', 'participants')
        }),
    )