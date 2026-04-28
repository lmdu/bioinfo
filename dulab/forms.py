from PIL import Image

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

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
