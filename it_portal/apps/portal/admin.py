from django.contrib import admin
from django import forms
from .models import Category, Article, Comment, ReplyComment, ArticleLike
# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
class ArticleLikeInline(admin.StackedInline):
    model = ArticleLike
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ CommentInline, ArticleLikeInline ]
    list_display = ('title', 'category', 'author', 'view', 'timestamp')
    list_display_links = ('title', 'category', 'author')

class ReplyCommentInline(admin.StackedInline):
    model = ReplyComment
    extra = 0

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    inlines = [ ReplyCommentInline ]
    list_display = ('article', 'author', 'content', 'timestamp')
    list_display_links = ('article', 'author', 'content')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')

admin.site.register(ArticleLike)