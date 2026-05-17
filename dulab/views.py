import os

from django.urls import reverse, reverse_lazy
from django.db.models import Sum, F
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
		context['supports'] = Option.objects.filter(slug__in=['genome', 'transcriptome', 'epigenome', 'translatome']).order_by('pk')

		return context

class NewsListView(ListView):
	model = Post
	paginate_by = 10
	template_name = 'dulab/news.html'
	queryset = Post.objects.filter(approve=1)

class PostDetailView(DetailView):
	model = Post
	template_name = 'dulab/post.html'

class PublicationListView(ListView):
	model = Publication
	template_name = 'dulab/publication.html'

class MemberListView(ListView):
	model = Member
	template_name = 'dulab/team.html'
	queryset = Member.objects.filter(allowed__gt=0).order_by('identity', 'position', 'degree', 'grade')

class MemberDetailView(DetailView):
	model = Member
	template_name = 'dulab/member.html'
	context_object_name = 'member'
	slug_field = 'user__username'

class ResearchListView(ListView):
	model = Research
	template_name = 'dulab/research.html'

class SoftwareListView(ListView):
	model = Software
	template_name = 'dulab/softwares.html'

class SoftwareDetailView(DetailView):
	model = Software
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

class SignoutView(LogoutView):
	next_page = reverse_lazy('dulab:index')

class PasswordSetView(LoginRequiredMixin, PasswordChangeView):
	template_name = 'dulab/setpasswd.html'
	success_url = reverse_lazy('dulab:signin')

	def form_valid(self, form):
		response = super().form_valid(form)
		logout(self.request)
		return response

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

class PhotoUploadView(LoginRequiredMixin, CreateView):
	model = Photo
	fields = ['image']

	def form_invalid(self, form):
		return JsonResponse({'errno': 1, 'message': form.errors.as_text()}, status=400)

	def form_valid(self, form):
		form.instance.author = self.request.user
		self.object = form.save()
		return JsonResponse({'errno': 0, 'data': {'url': self.object.image.url}})

class PhotoListView(LoginRequiredMixin, View):
	def post(self, request):
		photos = Photo.objects.filter(author=request.user)[0:12]
		urls = [p.image.url for p in photos]
		return JsonResponse({'photos': urls})

class AvatarDeleteView(LoginRequiredMixin, View):
	def post(self, request):
		profile = request.user.profile
		profile.avatar.delete()
		return JsonResponse({'success': True})

class PostListView(LoginRequiredMixin, ListView):
	model = Post
	paginate_by = 15
	template_name = 'dulab/postlist.html'

	def get_queryset(self):
		return Post.objects.filter(author=self.request.user)

class PostAddView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'dulab/postadd.html'
	success_url = reverse_lazy('dulab:postlist')

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostEditView(LoginRequiredMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = 'dulab/postedit.html'
	success_url = reverse_lazy('dulab:postlist')

	def form_valid(self, form):
		form.instance.approve = 0
		return super().form_valid(form)

class DownloadView(View):
	def get(self, request, did):
		d = get_object_or_404(Download, pk=did)
		d.visitor = F('visitor') + 1
		d.save()

		return FileResponse(d.package.open(), 
			as_attachment = True,
			filename = os.path.basename(d.package.name)
		)

