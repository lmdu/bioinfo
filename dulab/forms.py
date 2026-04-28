from PIL import Image

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from crispy_forms.bootstrap import Tab, TabHolder

from .models import *

class SignupForm(UserCreationForm):
	email = forms.EmailField(label=_("邮箱"), help_text=_("不要用QQ邮箱, 用于以后投稿"), required=True)
	name = forms.CharField(label=_("姓名"), help_text=_("输入真实姓名, 才能通过审核"), required=True)

	class Meta:
		model = User
		fields = ('username', 'name', 'email', 'password1', 'password2')

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
			user.profile.name_zh = self.cleaned_data['name']
			user.profile.save()

		return user

class ProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
			HTML('<h3 class="card-title mt-4"><strong>基本信息</strong></h3>'),
			Row(
				Column('name_zh', css_class='col-md-6'),
				Column('name_en', css_class='col-md-6'),
				Column('title_zh', css_class='col-md-6'),
				Column('title_en', css_class='col-md-6'),
				css_class = 'g-3'
			),
			HTML('<h3 class="card-title mt-4"><strong>专业研究</strong></h3>'),
			Row(
				Column('major_zh', css_class='col-md-6'),
				Column('major_en', css_class='col-md-6'),
				Column('direct_zh', css_class='col-md-6'),
				Column('direct_en', css_class='col-md-6'),
				css_class = 'g-3'
			),
			HTML('<h3 class="card-title mt-4"><strong>联系方式</strong></h3>'),
			Row(
				Column('phone', css_class='col-md-4 col-sm-6'),
				Column('qq', css_class='col-md-4 col-sm-6'),
				Column('weixin', css_class='col-md-4 col-sm-6'),
				css_class = 'g-3'
			),
			HTML('<h3 class="card-title mt-4"><strong>学籍信息</strong></h3>'),
			Row(
				Column('grade', css_class='col-md-4 col-sm-6'),
				Column('degree', css_class='col-md-4 col-sm-6'),
				Column('position', css_class='col-md-4 col-sm-6'),
				css_class = 'g-3'
			),
			HTML('<h3 class="card-title mt-4"><strong>学术链接</strong></h3>'),
			Row(
				Column('github', css_class='col-md-4 col-sm-6'),
				Column('researchgate', css_class='col-md-4 col-sm-6'),
				Column('google', css_class='col-md-4 col-sm-6'),
				css_class = 'g-3'
			),
			HTML('<h3 class="card-title mt-4"><strong>个人简介</strong></h3>'),
			TabHolder(
				Tab('中文', 'bio_zh'),
				Tab('英文', 'bio_en')
			)
		)

	class Meta:
		model = Member
		exclude = ('user', 'avatar', 'allowed', 'created')

class AvatarCropForm(forms.ModelForm):
	x = forms.FloatField(widget=forms.HiddenInput())
	y = forms.FloatField(widget=forms.HiddenInput())
	w = forms.FloatField(widget=forms.HiddenInput())
	h = forms.FloatField(widget=forms.HiddenInput())

	class Meta:
		model = Member
		fields = ['avatar', 'x', 'y', 'w', 'h']

	def save(self):
		profile = super().save()

		x = self.cleaned_data.get('x')
		y = self.cleaned_data.get('y')
		w = self.cleaned_data.get('w')
		h = self.cleaned_data.get('h')

		image = Image.open(profile.avatar)
		crop_img = image.crop((x, y, x+w, y+h))

		if w > 200:
			crop_img = crop_img.resize((200, 200), Image.ANTIALIAS)

		crop_img.save(profile.avatar.path)
		return profile
