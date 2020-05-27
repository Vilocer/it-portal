from django.contrib import admin
from .models import Profile, ProfileSubscriber
from apps.portal.models import Article, ArticleLike
# Register your models here.

class ArticlesInline(admin.TabularInline):
	model = Article
	extra = 0

class ProfileSubscriberInline(admin.StackedInline):
    model = ProfileSubscriber
    extra = 0

class ArticleLikeInline(admin.TabularInline):
	model = ArticleLike
	extra = 0

class ProfilesAdmin(admin.ModelAdmin):
    inlines = [ProfileSubscriberInline, ArticleLikeInline, ArticlesInline]

admin.site.register(Profile, ProfilesAdmin)
