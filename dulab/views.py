import os

from django.urls import reverse, reverse_lazy
from django.db.models import Sum
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.http import HttpResponseNotFound, JsonResponse, FileResponse
from django.views.generic import View, TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *

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
		context['introduce'] = Option.objects.filter(slug='introduce').first()
		context['interest'] = Option.objects.filter(slug='interest').first()
		context['supports'] = Option.objects.filter(slug='supports')

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

class SigninView(LoginView):
	next_page = reverse_lazy('dulab:index')
	template_name = 'dulab/signin.html'

class SignupView(CreateView):
	form_class = SignupForm
	success_url = reverse_lazy('dulab:signin')
	template_name = 'dulab/signup.html'

def signout(request):
	logout(request)
	return redirect('dulab:index')

class PasswordSetView(LoginRequiredMixin, PasswordChangeView):
	template_name = 'dulab/setpasswd.html'
	success_url = reverse_lazy('dulab:setpasswd')

class ProfileView(LoginRequiredMixin, UpdateView):
	model = Member
	form_class = ProfileForm
	template_name = 'dulab/profile.html'
	success_url = reverse_lazy('dulab:profile')

	def get_object(self, queryset=None):
		return Member.objects.get(user=self.request.user)

class AvatarUploadView(LoginRequiredMixin, View):
	def post(self, request):
		profile = self.request.user.profile
		profile.avatar.delete()
		form = AvatarCropForm(request.POST, request.FILES, instance=profile)

		if form.is_valid():
			form.save()
			return JsonResponse({'success': True, 'path': profile.avatar.url})

		return JsonResponse({'success': False})

class AvatarDeleteView(LoginRequiredMixin, View):
	def post(self, request):
		profile = self.request.user.profile
		profile.avatar.delete()
		return JsonResponse({'success': True})

class PostListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'dulab/postlist.html'

class PostAddView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'dulab/postadd.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostEditView(LoginRequiredMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = 'dulab/postadd.html'

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
