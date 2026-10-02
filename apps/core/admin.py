from django.contrib import admin
from apps.core.models import Work, Inquiry, Article

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'live_url', 'is_featured', 'is_published', 'sort_order', 'created_at')
    list_filter = ('category', 'is_featured', 'is_published')
    search_fields = ('title', 'client', 'summary', 'challenge', 'solution')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'is_published', 'sort_order')
    fieldsets = (
        ('Overview', {
            'fields': ('title', 'full_title', 'slug', 'client', 'category', 'year', 'live_url', 'image_url', 'sort_order')
        }),
        ('Narrative & Teaser', {
            'fields': ('summary', 'challenge', 'solution', 'deliverables_summary')
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_published')
        }),
    )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'reading_time', 'is_published', 'published_at')
    list_filter = ('category', 'is_published', 'published_at')
    search_fields = ('title', 'summary', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    fieldsets = (
        ('Article Metadata', {
            'fields': ('title', 'slug', 'category', 'author', 'reading_time', 'is_published')
        }),
        ('Article Content', {
            'fields': ('summary', 'content'),
            'description': 'Write in clean plain text or Markdown (use ### for subheadings, - for bullet points).'
        }),
    )

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'service_interest', 'budget_range', 'status', 'submitted_at')
    list_filter = ('status', 'service_interest', 'submitted_at')
    search_fields = ('full_name', 'email', 'message')
    list_editable = ('status',)
    readonly_fields = ('submitted_at',)
