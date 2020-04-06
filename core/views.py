# CORE VIEWS.PY


from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from .models import Article # Our model of Article (textfield, datefield)
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # Class for working with list, views, creating, update and del
from django.views.generic.edit import FormMixin
from .forms import ArticleForm, AuthUserForm, RegisterUserForm, CommentForm # Class for working with forms
from django.urls import reverse, reverse_lazy # for redirect
from django.contrib import messages # status of require
from django.contrib.auth.views import LoginView, LogoutView # class for woking with logins
from django.contrib.auth.models import User # get model of User (name, password)
from django.contrib.auth import authenticate, login # get class of auth and login
from django.contrib.auth.mixins import LoginRequiredMixin # get login from form
from django.http import HttpResponseRedirect # get http redirect 



# HOME VIEW FUNCTION
# def home(request):
# 	list_articles = Article.objects.all()
# 	context = {
# 		'list_articles': list_articles,
# 	}
# 	template = 'index.html'
# 	return render(request, template, context)

# DETAIL VIEW FUNCTION
# def detail_page(request, id):
# 	get_article = Article.objects.get(id = id)
# 	context = {
# 		'get_article': get_article,
# 	}
# 	template = 'detail.html'
# 	return render(request, template, context)

# EDIT FUNCTION
# def edit(request):
# 	success = False

# 	if request.method == 'POST':
# 		form = ArticleForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			success = True

# 	template = 'edit.html'
# 	context = {
# 		'list_articles': Article.objects.all().order_by('-id'),
# 		'form': ArticleForm(),
# 		'success': success,
# 	}
# 	return render(request, template, context)

# UPDATE FUNCTION
# def update(request, pk):
# 	success_update = False
# 	get_article = Article.objects.get(pk = pk)

# 	if request.method == 'POST':
# 		form = ArticleForm(request.POST, instance = get_article)
# 		if form.is_valid():
# 			form.save()
# 			success_update = True

# 	template = 'edit.html'

# 	context = {
# 		'get_article': get_article,
# 		'form': ArticleForm(instance = get_article),
# 		'update': True,
# 		'success_update': success_update,
# 	}
# 	return render(request, template, context)

# DELETE FUNCTION
# def delete(request, pk):
# 	get_article = Article.objects.get(pk = pk)
# 	get_article.delete()
# 	return redirect(reverse('edit'))

class CustomSuccessMessageMixin:

	@property
	def success_msg(self):
		return False
	def form_valid(self, form):
		messages.success(self.request, self.success_msg)
		return super().form_valid(form)

class HomeListView(ListView):
	model = Article
	template_name = 'index.html'
	context_object_name = 'list_articles'



class HomeDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
	model = Article
	template_name = 'detail.html'
	context_object_name = 'get_article'
	form_class = CommentForm
	success_msg = 'Комментарий создан, ожидайте модерации'

	def get_success_url(self, **kwargs): # title what it was (success or error)
		return reverse_lazy('detail_page', kwargs = {'pk': self.get_object().id})

	def post(self, request, *args, **kwargs):
		form = self.get_form() # we have form that we send it
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid()

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.article = self.get_object()
		self.object.author = self.request.user
		self.object.save()
		return super().form_valid(form)



class ArticleCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView): # Inheritance of class CustomSuccessMessageMixin
	login_url = reverse_lazy('login')
	model = Article
	template_name = 'edit.html'

	form_class = ArticleForm # Call forms
	success_url = reverse_lazy('edit') # slowly call reverse (redirect)

	success_msg = 'Запись создана' # Send Success Message

	def get_context_data(self, **kwargs): # redefine context info (list_articles)
		kwargs['list_articles'] = Article.objects.all().order_by('-id')
		return super().get_context_data(**kwargs)

	def get_success_url(self): # title what it was
		return '%s?id=%s' % (self.success_url, self.object.id)

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.author = self.request.user
		self.object.save()
		return super().form_valid(form)




class ArticleUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
	model = Article
	template_name = 'edit.html'

	form_class = ArticleForm
	success_url = reverse_lazy('edit')

	success_msg = 'Запись обновлена'

	def get_context_data(self, **kwargs):
		kwargs['update'] = True
		return super().get_context_data(**kwargs)

	def get_success_url(self): # title what it was
		return '%s?id=%s' % (self.success_url, self.object.id)

	def get_form_kwargs(self): # redefine and getting initial this class
		kwargs = super().get_form_kwargs()
		if self.request.user != kwargs['instance'].author:
			return self.handle_no_permission()
		return kwargs


class ProjectLoginView(LoginView): # Authentification page
	template_name = 'login.html'
	form_class = AuthUserForm
	success_url = reverse_lazy('edit')
	def get_success_url(self): # ReDirect not default 'accounts/profile' to 'edit page'
		return self.success_url



class ProjectJoinView(CreateView):
	model = User
	template_name = 'join.html'

	form_class = RegisterUserForm
	success_url = reverse_lazy('edit')

	success_msg = 'Пользователь успешно создан'
	def form_valid(self, form):
		form_valid = super().form_valid(form)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		aut_user = authenticate(username=username, password=password)
		login(self.request, aut_user)
		return form_valid


class ProjectLogout(LogoutView):
	next_page = reverse_lazy('edit')


class ArticleDeleteView(LoginRequiredMixin, DeleteView): # Inheritance of class CustomSuccessMessageMixin WILL NOT WORKING with this CLASS, because type = 'POST'
	model = Article
	template_name = 'edit.html'
	success_url = reverse_lazy('edit')

	success_msg = 'Запись удалена'

	def post(self, request, *args, **kwargs):
		messages.success(self.request, self.success_msg)
		return super().post(request) # get method post and type request

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.author
		self.request.user

		if self.request.user != self.object.author: # if no permission, then dont have access
			return self.handle_no_permission()


		success_url = self.get_success_url()
		self.object.delete()
		return HttpResponseRedirect(success_url)




