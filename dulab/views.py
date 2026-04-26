import os

from django.urls import reverse
from django.db.models import Sum
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseNotFound, JsonResponse, FileResponse
from django.views.generic import View, TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *

# Create your views here.
class IndexView(TemplateView):
	template_name = 'dulab/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		slides = Slideshow.objects.all()[0:5]
		context['slides'] = slides
		context['sliden'] = slides.count()
		context['papers'] = Publication.objects.all()[0:5]
		context['posts'] = Post.objects.filter(approve=1)[0:8]
		context['introduce'] = Option.objects.filter(name='introduce').first()
		context['interest'] = Option.objects.filter(name='interest').first()
		context['supports'] = Option.objects.filter(name='supports')

		return context

class PostListView(ListView):
	model = Post
	template_name = 'dulab/news.html'
	context_object_name = 'posts'
	paginate_by = 10

class PostDetailView(DetailView):
	model = Post
	template_name = 'dulab/post.html'

class PublicationListView(ListView):
	model = Publication
	template_name = 'dulab/publication.html'

class MemberListView(TemplateView):
	template_name = 'dulab/team.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		context['faculties'] = Member.objects.filter(position=4)
		context['postgraduates'] = Member.objects.filter(position=1, status=1)
		context['undergraduates'] = Member.objects.filter(position=2, status=1)
		context['graduates'] = Member.objects.filter(status=2)

		return context

class MemberDetailView(DetailView):
	model = Member
	template_name = 'dulab/member.html'
	context_object_name = 'member'
	slug_field = 'profile__username'

class ResearchListView(ListView):
	model = Research
	template_name = 'dulab/research.html'

class SoftwareListView(ListView):
	model = Software
	template_name = 'dulab/softwares.html'

class SoftwareDetailView(DetailView):
	template_name = 'dulab/software.html'

class PageDetailView(DetailView):
	page_name = None
	template_name = 'dulab/page.html'

	def get_object(self):
		return get_object_or_404(Option, slug=self.page_name)

class AboutDetailView(PageDetailView):
	page_name = 'aboutus'

class JoinusDetailView(PageDetailView):
	page_name = 'joinus'

class ContactDetailView(PageDetailView):
	page_name = 'contactus'

def signin(request):
	if request.method == 'GET':
		return render(request, 'big/signin.html')

	else:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			member = Member.objects.get(uname=username)
			if member.avatar:
				request.session['avatar'] = member.avatar.url
			else:
				request.session['avatar'] = None

			return redirect('big:profile')

		else:
			messages.add_message(request, messages.ERROR, _("用户名或密码错误, 忘记帐号密码请联系管理员"))
			return redirect('big:signin')

class SignoutView(LogoutView):
	pass

def signout(request):
	logout(request)
	return redirect('big:index')

def signup(request):
	if request.method == 'GET':
		return render(request, 'big/signup.html')

	elif request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		name = request.POST.get('name')
		password = request.POST.get('password')

		if len(username) < 4:
			messages.add_message(request, messages.WARNING, _("用户名长度至少为4位字母"))

		elif User.objects.filter(username=username).exists():
			messages.add_message(request, messages.WARNING, _("你输入的用户名已被占用, 请重新输入用户名"))
		
		elif len(password) < 8:
			messages.add_message(request, messages.WARNING, _("密码的长度至少为8位数字或字母"))
		
		else:
			User.objects.create_user(
				username = username,
				password = password,
				email = email,
			)
			Member.objects.create_user(
				uname = username,
				email = email,
			)

			messages.add_message(request, messages.SUCCESS,
			 _('注册成功, 请 <a href="{}">登录</a> 系统, 修改个人资料'.format(reverse('big:signin'))))

		return redirect('big:signup')

@login_required(login_url='/signin')
def profile(request):
	if request.method == 'GET':
		member = Member.objects.get(uname=request.user.username)
		return render(request, 'big/profile.html', {'member': member})

	elif request.method == 'POST':
		data = request.POST
		avatar = request.FILES.get('avatar', None)
		member = Member.objects.get(uname=request.user.username)
		
		if avatar:
			member.avatar = avatar

		member.email = data['email']
		member.name_zh = data['name_zh']
		member.name_en = data['name_en']
		member.title_zh = data['title_zh']
		member.title_en = data['title_en']
		member.phone = data['phone']
		member.major_zh = data['major_zh']
		member.major_en = data['major_en']
		member.grade = int(data['grade'])
		member.degree = int(data['degree'])
		member.position = int(data['position'])
		member.status = int(data['status'])
		member.direct_zh = data['direct_zh']
		member.direct_en = data['direct_en']
		member.bio_zh = data['bio_zh']
		member.bio_en = data['bio_en']
		member.github = data['github']
		member.researchgate = data['researchgate']
		member.google = data['google']
		member.save()

		return redirect('big:profile')

@login_required(login_url='/signin')
def resetpasswd(request):
	if request.method == 'GET':
		return render(request, 'big/resetpasswd.html')

	elif request.method == 'POST':
		oldpasswd = request.POST.get('oldpasswd')
		newpasswd = request.POST.get('newpasswd')
		okpasswd = request.POST.get('okpasswd')

		if len(newpasswd) < 8:
			messages.add_message(request, messages.WARNING, _("密码的长度至少为8位数字或字母"))

		elif newpasswd != okpasswd:
			messages.add_message(request, messages.WARNING, _("两次输入的密码不一致"))

		elif authenticate(username=request.user.username, password=oldpasswd) is None:
			messages.add_message(request, messages.WARNING, _("旧密码不正确"))

		else:
			user = User.objects.get(pk=request.user.id)
			user.set_password(newpasswd)
			user.save()
			return redirect('big:signin')

		return redirect('big:resetpasswd')

@login_required(login_url='/signin')
def postadd(request):
	if request.method == 'GET':
		return render(request, 'big/postadd.html')

	elif request.method == 'POST':
		data = request.POST

		if Post.objects.filter(slug=data['slug']).exists():
			messages.add_message(request, messages.WARNING, _("别名已被占用, 请重新输入"))
			return redirect('big:postadd')

		author = Member.objects.get(uname=request.user.username)

		post = Post.objects.create(
			slug = data['slug'],
			title_zh = data['title_zh'],
			title_en = data['title_en'],
			content_zh = data['content_zh'],
			content_en = data['content_en'],
			author = author,
		)

		img = request.FILES.get('thumbnail', None)
		if img:
			post.thumbnail = img
			post.save()

		return redirect('big:postlist')

@login_required(login_url='/signin')
def postlist(request):
	if request.method == 'GET':
		#member = Member.objects.get(uname=request.user.username)
		post_list = Post.objects.filter(author__uname=request.user.username)
		paginator = Paginator(post_list, 15)
		page = request.GET.get('page')
		posts = paginator.get_page(page)

		return render(request, 'big/postlist.html', {'posts': posts})

@login_required(login_url='/signin')
def postedit(request, slug):
	if request.method == 'GET':
		post = Post.objects.get(slug=slug)
		return render(request, 'big/postedit.html', {'post': post})

	elif request.method == 'POST':
		data = request.POST
		post = Post.objects.get(slug=slug)
		
		if slug != data['slug']:
			if Post.objects.filter(slug=data['slug']).exists():
				messages.add_message(request, messages.WARNING, _("别名已被占用, 请重新输入"))
				return redirect(reverse('big:postedit', kwargs={'slug':slug}))
		
		post.slug = data['slug']
		post.title_zh = data['title_zh']
		post.title_en = data['title_en']
		post.content_zh = data['content_zh']
		post.content_en = data['content_en']
		post.approve = 0

		img = request.FILES.get('thumbnail', None)
		if img:
			post.thumbnail = img
		post.save()

		return redirect('big:postlist')

@login_required(login_url='/signin')
def postdelete(request, slug):
	if request.method == 'GET':
		Post.objects.get(slug=slug).delete()
		return redirect('big:postlist')

@login_required
def upload(request):
	if request.method == 'POST':
		files = request.FILES.getlist('files')

		medias = []
		isimgs = []
		msgs = []
		for file in files:
			media = Media.objects.create(
				name = file.name,
				file = file,
				ctype = file.content_type,
				size = file.size,
			)

			medias.append(media.file.url)
			isimgs.append(media.ctype.startswith('image'))
			msgs.append(media.name)

		return JsonResponse({
			'success': True,
			'time': '',
			'data': {
				'baseurl': '',
				'files': medias,
				'isImages': isimgs,
				'messages': msgs,
			}
		})

@login_required
def browser(request):
	if request.method == 'POST':
		medias = []
		for media in Media.objects.all():
			medias.append({
				'file': media.file.url,
				'name': media.name,
				'size': media.size,
				'isImage': media.ctype.startswith('image'),
			})

		return JsonResponse({
			'success': True,
			'time': '',
			'data': {
				'sources': {
					'a': {
						'path': '',
						'baseurl': '',
						'files': medias,
						'folders': '',
					}
				},
				'code': 200,
				'path': '',
				'name': '',
				'source': '',
			}
		})

@login_required(login_url='/signin')
def fund(request):
	funds = Fund.objects.all()
	return render(request, 'big/fund.html', {'funds':funds})

@login_required(login_url='/signin')
def expense(request, fid):
	fid = int(fid)
	fund = Fund.objects.get(pk=fid)
	expenses = Expense.objects.filter(fund__pk=fid)
	expend = Expense.objects.filter(fund__pk=fid).aggregate(money=Sum('amount'))

	if expend['money'] is None:
		expend['money'] = 0

	return render(request, 'big/expense.html', {
		'expenses':expenses, 'fund':fund,
		'expend': expend
	})
