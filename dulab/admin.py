from django.db import models

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import *

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
	# Forms loaded from `unfold.forms`
	form = UserChangeForm
	add_form = UserCreationForm
	change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
	pass

@admin.register(Slideshow)
class SlideAdmin(ModelAdmin):
	list_display = ('title_zh', 'show_slide', 'link', 'created')

	@display(description='slideshow')
	def show_slide(self, obj):
		if obj.slide:
			if obj.slide.url.endswith('.mp4'):
				return format_html('<video src="{}" class="w-80 object-cover" controls></video>', obj.slide.url)
			else:
				return format_html('<img src="{}" class="w-80 object-cover">', obj.slide.url)

		return 'No slide'

@admin.register(Post)
class PostAdmin(ModelAdmin):
	list_display = ('slug', 'title_zh', 'approve_category', 'created')
	search_fields = ('title_zh',)

	@display(label={0: 'danger', 1: 'success', 2: 'info'}, description="审核")
	def approve_category(self, obj):
		return obj.approve, obj.get_approve_display()

@admin.register(Publication)
class PublicationAdmin(ModelAdmin):
	list_display = ('title', 'journal', 'year', 'factor', 'created')
	list_filter = ('journal', 'year')
	search_fields = ('title', 'authors')

@admin.register(Research)
class ResearchAdmin(ModelAdmin):
	list_display = ('direction_zh', 'show_thumbnail', 'rank', 'created')

	@display(description="缩略图")
	def show_thumbnail(self, obj):
		if obj.thumbnail:
			return format_html('<img src="{}" class="w-80 object-cover">', obj.thumbnail.url)

@admin.register(Member)
class MemberAdmin(ModelAdmin):
	list_display = ('user__username', 'user__email', 'name_zh', 'number', 'phone', 'qq', 'weixin',
	 'major_zh', 'grade', 'degree', 'position', 'identity', 'show_allowed')
	list_filter = ('degree', 'identity')
	search_fields = ('user__username', 'name_zh')

	@display(label={0: 'danger', 1: 'success', 2: 'warning'})
	def show_allowed(self, obj):
		return obj.allowed, obj.get_allowed_display()

@admin.register(Software)
class SoftwareAdmin(ModelAdmin):
	list_display = ('slug', 'show_logo', 'name_zh', 'url', 'category', 'title_zh', 'created')

	@display(header=True, description='Logo')
	def show_logo(self, obj):
		if obj.logo:
			return [
				None, None, None,
				{
					'path': obj.logo.url
				}
			]

@admin.register(Version)
class VersionAdmin(ModelAdmin):
	list_display = ('version', 'software', 'created')

@admin.register(Download)
class DownloadAdmin(ModelAdmin):
	list_display = ('version', 'system', 'name', 'package', 'visitor', 'uploaded')
	list_filter = ('system',)
	search_fields = ('version', 'package', 'name')

@admin.register(Photo)
class PhotoAdmin(ModelAdmin):
	list_display = ('show_image', 'author', 'uploaded')

	@display(description='image')
	def show_image(self, obj):
		if obj.image:
			return format_html('<img src="{}" class="w-80 object-cover">', obj.image.url)

@admin.register(Option)
class OptionAdmin(ModelAdmin):
	list_display = ('slug', 'title_zh', 'content_zh', 'created')

