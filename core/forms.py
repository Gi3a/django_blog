from django import forms
from django.forms import Textarea
from .models import Article, Comment

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ('name', 'text')
	def __init__(self, *args, **kwargs): # Connect bootstrap styles for input's
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

class AuthUserForm(AuthenticationForm, forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

class RegisterUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'
	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text',)
	def __init__(self, *args, **kwargs): # Connect bootstrap styles for input's
		super().__init__(*args, **kwargs)
		self.fields['text'].widget = Textarea(attrs={'rows': 5})
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'