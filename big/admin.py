from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'slug')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'excerpt', 'layout', 'category', 'created')
	list_filter = ('category__name', 'layout')
	search_fields = ('title',)

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'journal', 'factor', 'created')
	list_filter = ('journal',)
	search_fields = ('title',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'slug', 'title', 'email', 'degree')
	list_filter = ('degree',)
	search_fields = ('name',)

@admin.register(Slideshow)
class SlideAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'image', 'article', 'created')
