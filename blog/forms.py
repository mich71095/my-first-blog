from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment, Profile

#from ckeditor_uploader.widgets import CKEditorUploadingWidget
#from ckeditor.widgets import CKEditorWidget

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget





class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		#text = forms.CharField(widget=CKEditorUploadingWidget())
		#post_description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'post ni description'}))
		#cover_pic = forms.ImageField(widget=forms.ClearableFileInput(attrs={'onchange': 'previewFile()', 'class': 'filePreviewImage'}))
		#title = forms.CharField(widget=forms.TextInput(attrs={'size':34,'placeholder':'username'}))
		fields = ('title', 'text', 'cover_pic', 'post_description')
		#summernote
		widgets = {
		'text': SummernoteWidget(),
		'title': forms.TextInput(attrs={'size':34,'placeholder':'post title'}),
		'post_description': forms.TextInput(attrs={'placeholder': 'post ni description'}),
		'cover_pic': forms.ClearableFileInput(attrs={'onchange': 'preview()', 'class': 'previewImage'}),
		}
		
'''class PostForm(forms.Form):
	model = Post
	#fields = ('title', 'text',)
	foo = forms.CharField(widget=SummernoteWidget)'''

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ( 'text',)

class NonAdminAccountForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'size':34,'placeholder':'username'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'size':34,'placeholder':'first name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'size':34,'placeholder':'last name'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'size':34,'placeholder':'email'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'size':34,'placeholder':'password'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'size':34,'placeholder':'confirm password'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

'''class UserForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'size':34,'placeholder':'username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'size':34,'placeholder':'password'}))
	class Meta:
		model = User
		fields = ('username','first_name', 'last_name', 'email')'''

class LoginForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'size':34,'placeholder':'username'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'size':34,'placeholder':'password'}))

	class Meta:
		model = User
		fields = ('username','password1')

class ProfileForm(forms.ModelForm):
	location = forms.CharField(required=False)
	birth_date = forms.DateField(required=False)
	gender = forms.CharField(required=False)
	lives = forms.CharField(required=False)
	status = forms.CharField(required=False)
	studied = forms.CharField(required=False)
	profession = forms.CharField(required=False)
	language = forms.CharField(required=False)
	motto = forms.CharField(required=False)

	class Meta:
		model = Profile
		fields = ( 'user_cover_pic','user_profile_pic','bio', 'location','birth_date','gender','lives','status', 'work','studied','profession','language','motto','about_me')
		widgets = {
			'location': forms.TextInput(attrs={'size':34,'placeholder':'homwtown'}),
			'birth_date': forms.TextInput(attrs={'size':34,'placeholder':'birthday'}),
			'gender': forms.TextInput(attrs={'size':34,'placeholder':'gender'}),
			'lives': forms.TextInput(attrs={'size':34,'placeholder':'currenty lives'}),
			'status': forms.TextInput(attrs={'size':34,'placeholder':'status'}),
			'studied': forms.TextInput(attrs={'size':34,'placeholder':'school'}),
			'profession': forms.TextInput(attrs={'size':34,'placeholder':'profession'}),
			'language': forms.TextInput(attrs={'size':34,'placeholder':'language spoken'}),
			'motto': forms.TextInput(attrs={'size':34,'placeholder':'motto in life'}),
			'user_cover_pic': forms.ClearableFileInput(attrs={'onchange': 'previewUserCover()', 'class': 'previewImageUserCover'}),
			'user_profile_pic': forms.ClearableFileInput(attrs={'onchange': 'previewUser()', 'class': 'previewImageUser'}),
		}

