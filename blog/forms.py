from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment

#from ckeditor_uploader.widgets import CKEditorUploadingWidget
#from ckeditor.widgets import CKEditorWidget

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		#text = forms.CharField(widget=CKEditorUploadingWidget())
		fields = ('title', 'text',)
		#summernote
		widgets = {
		'text': SummernoteWidget(),
		}
		
'''class PostForm(forms.Form):
	model = Post
	#fields = ('title', 'text',)
	foo = forms.CharField(widget=SummernoteWidget)'''

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('author', 'text',)

class RegisterAccountForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
	last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
	email = forms.EmailField(max_length=254, required=True, help_text='Required. Email should valid')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )