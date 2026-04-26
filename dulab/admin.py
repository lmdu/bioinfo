from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

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
	list_display = ('id', 'title_zh', 'slide', 'link', 'created')

@admin.register(Post)
class PostAdmin(ModelAdmin):
	list_display = ('id', 'title_zh', 'created', 'updated')
	search_fields = ('title_zh',)

@admin.register(Publication)
class PublicationAdmin(ModelAdmin):
	list_display = ('id', 'title', 'journal', 'factor', 'created')
	list_filter = ('journal',)
	search_fields = ('title',)

@admin.register(Research)
class ResearchAdmin(ModelAdmin):
	list_display = ('id', 'direction_zh', 'rank', 'created')

@admin.register(Member)
class MemberAdmin(ModelAdmin):
	list_display = ('id', 'major_zh', 'grade', 'degree', 'position', 'status')
	list_filter = ('degree',)

@admin.register(Software)
class SoftwareAdmin(ModelAdmin):
	list_display = ('id', 'name_zh', 'url', 'category', 'description_zh', 'created')

@admin.register(Version)
class VersionAdmin(ModelAdmin):
	list_display = ('id', 'version', 'software', 'created')

@admin.register(Download)
class DownloadAdmin(ModelAdmin):
	list_display = ('id', 'system', 'package', 'uploaded', 'version')

@admin.register(Media)
class MediaAdmin(ModelAdmin):
	list_display = ('id', 'file', 'ctype', 'size', 'uploaded')

@admin.register(Option)
class OptionAdmin(ModelAdmin):
	list_display = ('id', 'name', 'title_zh', 'content_zh', 'created')

@admin.register(Fund)
class FundAdmin(ModelAdmin):
	list_display = ('id', 'name', 'category', 'approve_code', 'approve_amount', 'approve_time')

@admin.register(Expense)
class ExpenseAdmin(ModelAdmin):
	list_display = ('id', 'fund', 'category', 'amount', 'created')

