from django.contrib import admin
from .models import Post, Comment, Image, Profile

class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'user']
    inlines = [CommentsInline]

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Profile)
