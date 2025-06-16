from django.contrib import admin
from django.utils.html import format_html
from .models import *
from django.utils.html import format_html


# Register your models here.

admin.site.register(Category)
admin.site.register(Comment)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'blog_slug', 'seo_score']

    def seo_score(self, obj):
        score = obj.keyword_score()

        # Color logic
        if score >= 80:
            color = 'green'
        elif score >= 50:
            color = 'orange'
        else:
            color = 'red'

        return format_html(
            f'<strong style="color:{color};">{score}% SEO Score</strong>'
        )

    seo_score.short_description = "SEO Score"
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="120" height="auto" style="border-radius: 4px;" />', obj.image.url)
        return "No image"

    image_preview.short_description = 'Image Preview'
    fieldsets = (
        ('Blog Details', {
            'fields': (
                'title','blog_slug', 'author', 'image', 'image_preview', 'content', 'category', 'status', 'section', 'Main_post',
            )
        }),
        ('SEO Settings', {
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
            ),
            # 'classes': ('collapse',),  # Optional: make this section collapsible in admin
        }),
    )

    readonly_fields = ('image_preview',)



