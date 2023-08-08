from django.contrib import admin

from blog_app.models import Article, Comment 

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'author', 'display_tags']
    list_filter = ['tags', 'author']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created_at']
    list_filter = ['user']