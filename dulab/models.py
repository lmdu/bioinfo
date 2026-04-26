from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete, post_save

# Create your models here.
class BaseModel(models.Model):
	def __getattr__(self, attr):
		if attr not in self.__dict__:
			lang = get_language().split('-')[0]
			key = "{}_{}".format(attr, lang)

			if key in self.__dict__:
				return self.__dict__[key]

		return super().__getattr__(attr)

	class Meta:
		abstract = True

class Publication(BaseModel):
	title = models.CharField(max_length=255)
	abstract = models.TextField(blank=True)
	authors = models.TextField()
	journal = models.CharField(max_length=100)
	year = models.SmallIntegerField()
	volume = models.CharField(max_length=10, blank=True)
	issue = models.CharField(max_length=10, blank=True)
	pages = models.CharField(max_length=20, blank=True)
	doi = models.CharField(max_length=100)
	pmid = models.CharField(max_length=30, blank=True)
	factor = models.FloatField(default=0, blank=True)
	cover = models.ImageField(upload_to='dulab/thumbnails/', blank=True)
	pdf = models.FileField(upload_to='dulab/papers/', blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created']

class Member(BaseModel):
	DEGREES = {
		0: _("未设置"),
		1: _("博士"),
		2: _("硕士"),
		3: _("学士"),
	}

	POSITIONS = {
		0: _("未设置"),
		1: _("研究生"),
		2: _("本科生"),
		3: _("博士后"),
		4: _("教职工"),
		5: _("访问学者"),
	}

	STATUS = {
		0: _("未设置"),
		1: _("在读"),
		2: _("毕业"),
		3: _("退学"),
	}

	ALLOWS = {
		0: _("待审"),
		1: _("通过"),
	}

	YEARS = ((i, i) for i in range(2020, timezone.now().year+1))

	profile = models.OneToOneField(User, on_delete=models.CASCADE)
	name_zh = models.CharField(max_length=30, blank=True)
	name_en = models.CharField(max_length=30, blank=True)
	title_zh = models.CharField(max_length=255, blank=True)
	title_en = models.CharField(max_length=255, blank=True)
	phone = models.CharField(max_length=15, blank=True)
	qq = models.CharField(max_length=20, blank=True)
	weixin = models.CharField(max_length=30, blank=True)
	major_zh = models.CharField(max_length=30, blank=True)
	major_en = models.CharField(max_length=50, blank=True)
	grade = models.IntegerField(choices=YEARS, blank=True, default=2020)
	degree = models.SmallIntegerField(choices=DEGREES, blank=True, default=0)
	position = models.SmallIntegerField(choices=POSITIONS, blank=True, default=0)
	status = models.SmallIntegerField(choices=STATUS, blank=True, default=0)
	direct_zh = models.CharField(max_length=255, blank=True)
	direct_en = models.CharField(max_length=255, blank=True)
	avatar = models.ImageField(upload_to='dulab/avatars/', blank=True)
	bio_zh = models.TextField(blank=True)
	bio_en = models.TextField(blank=True)
	github = models.CharField(max_length=255, blank=True)
	researchgate = models.CharField(max_length=255, blank=True)
	google = models.CharField(max_length=255, blank=True)
	allowed = models.SmallIntegerField(choices=ALLOWS, blank=True, default=0)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name_zh

	class Meta:
		ordering = ['degree', 'grade']

@receiver(post_save, sender=User)
def create_member(sender, instance, created, **kwargs):
	if created:
		Member.objects.create(profile=instance)

@receiver(post_save, sender=User)
def save_member(sender, instance, **kwargs):
	instance.member.save()

class Post(BaseModel):
	APPROVES = {
		0: _("等待审核"),
		1: _("通过审核"),
		2: _("退回修改"),
	}

	slug = models.SlugField(unique=True)
	title_zh = models.CharField(max_length=255)
	title_en = models.CharField(max_length=255, blank=True)
	content_zh = models.TextField(blank=True)
	content_en = models.TextField(blank=True)
	thumbnail = models.ImageField(upload_to='dulab/thumbnails/', blank=True)
	banner = models.ImageField(upload_to='dulab/banners/', blank=True)
	approve = models.SmallIntegerField(choices=APPROVES, default=0)
	author = models.ForeignKey(Member, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created']

class Slideshow(BaseModel):
	title_zh = models.CharField(max_length=255, blank=True)
	title_en = models.CharField(max_length=255, blank=True)
	description_zh = models.TextField(blank=True)
	description_en = models.TextField(blank=True)
	slide = models.ImageField(upload_to='dulab/slides/')
	link = models.CharField(max_length=255, blank=True)
	extra_zh = models.TextField(blank=True)
	extra_en = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created']

class Software(BaseModel):
	TYPES = (
		(1, _("软件")),
		(2, _("数据库"))
	)

	slug = models.SlugField(unique=True)
	name_zh = models.CharField(max_length=100)
	name_en = models.CharField(max_length=100, blank=True)
	url = models.CharField(max_length=255, blank=True)
	doc = models.CharField(max_length=255, blank=True)
	language = models.CharField(max_length=30, blank=True)
	category = models.SmallIntegerField(choices=TYPES, default=0)
	comment_zh = models.TextField(blank=True)
	comment_en = models.TextField(blank=True)
	description_zh = models.TextField(blank=True)
	description_en = models.TextField(blank=True)
	thumbnail = models.ImageField(upload_to='dulab/thumbnails/', blank=True)
	logo = models.ImageField(upload_to='dulab/thumbnails/', blank=True)
	citation = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-created']

class Version(BaseModel):
	version = models.CharField(max_length=20)
	changelog_zh = models.TextField(blank=True)
	changelog_en = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	software = models.ForeignKey(Software, on_delete=models.CASCADE)

	def __str__(self):
		return '{} - {}'.format(self.software, self.version)

	class Meta:
		ordering = ['-created']

class Download(BaseModel):
	SYSTEMS = {
		0: 'Unknown',
		1: 'Windows',
		2: 'MacOS',
		3: 'Linux',
		4: 'Ubuntu',
		5: 'Fedora',
		6: 'Debian',
		7: 'RedHat',
		8: 'ArchLinux',
		9: 'openSUSE',
		10: 'AlmaLinux',
		11: 'Deepin',
		12: 'Centos',
		13: 'RockyLinux',
	}

	system = models.SmallIntegerField(choices=SYSTEMS, default=0)
	comment_zh = models.CharField(max_length=255, blank=True)
	comment_en = models.CharField(max_length=255, blank=True)
	package = models.FileField(upload_to='dulab/files/%Y/%m')
	represent = models.BooleanField(default=False)
	uploaded = models.DateTimeField(auto_now_add=True)
	version = models.ForeignKey(Version, on_delete=models.CASCADE)

	def __str__(self):
		return self.package.name

	class Meta:
		ordering = ['-uploaded']

class Research(BaseModel):
	direction_zh = models.TextField()
	direction_en = models.TextField(blank=True)
	thumbnail = models.ImageField(upload_to='dulab/thumbnails/')
	rank = models.SmallIntegerField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['rank']

class Media(BaseModel):
	name = models.CharField(max_length=255)
	file = models.FileField(upload_to='dulab/files/%Y/%m')
	ctype = models.CharField(max_length=100, blank=True)
	size = models.IntegerField()
	uploaded = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-uploaded']

class Option(BaseModel):
	slug = models.SlugField(unique=True)
	title_zh = models.CharField(max_length=255, blank=True)
	title_en = models.CharField(max_length=255, blank=True)
	content_zh = models.TextField(blank=True)
	content_en = models.TextField(blank=True)
	thumbnail = models.ImageField(upload_to='dulab/thumbnails', blank=True)
	created = models.DateTimeField(auto_now_add=True)

class Fund(BaseModel):	
	name = models.CharField(max_length=255)
	approve_code = models.CharField(max_length=50, blank=True)
	finance_code = models.CharField(max_length=50, blank=True)
	category = models.CharField(max_length=50, blank=True)
	source = models.CharField(max_length=255, blank=True)
	approve_amount = models.FloatField(default=0)
	approve_time = models.DateField(blank=True)
	start_time = models.DateField(blank=True)
	end_time = models.DateField(blank=True)
	comment = models.TextField(blank=True)
	create_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-create_time']

class Expense(BaseModel):
	CATEGORIES = {
		0: _("其他费"),
		1: _("材料费"),
		2: _("测序费"),
		3: _("设备费"),
		4: _("劳务费"),
		5: _("差旅费"),
		6: _("版面费"),
		7: _("咨询费"),
		8: _("绩效"),
		9: _("管理费"),
		10: _("税费"),
	}

	fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
	category = models.SmallIntegerField(choices=CATEGORIES, default=0)
	amount = models.FloatField()
	company = models.CharField(max_length=255, blank=True)
	invoice = models.FileField(upload_to='dulab/invoices/%Y/%m', blank=True)
	ticket = models.FileField(upload_to='dulab/tickets/%Y/%m', blank=True)
	comment = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created']

@receiver(pre_delete, sender=Slideshow)
def delete_slide(sender, instance, **kwargs):
	instance.image.delete(True)

@receiver(pre_delete, sender=Post)
def delete_post(sender, instance, **kwargs):
	instance.thumbnail.delete(True)

@receiver(pre_delete, sender=Member)
def delete_member(sender, instance, **kwargs):
	instance.avatar.delete(True)

@receiver(pre_delete, sender=Publication)
def delete_publication(sender, instance, **kwargs):
	instance.thumbnail.delete(True)

@receiver(pre_delete, sender=Software)
def delete_software(sender, instance, **kwargs):
	instance.thumbnail.delete(True)

@receiver(pre_delete, sender=Media)
def delete_media(sender, instance, **kwargs):
	instance.file.delete(True)

@receiver(pre_delete, sender=Research)
def delete_research(sender, instance, **kwargs):
	instance.thumbnail.delete(True)
