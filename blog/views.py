from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm, NonAdminAccountForm, ProfileForm, LoginForm
from django.contrib.auth.models import User

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse

from django.contrib.postgres.search import SearchVector

from hitcount.views import HitCountDetailView

# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']


@login_required
def logout_user(request):
	logout(request)
	return redirect('index')

def detail(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'blog/detail.html', {'album': album,})

'''@login_required
@transaction.atomic
def update_profile(request):
	#user = User.objects.get(pk=user_id)
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			#messages.add_message(request, "Your profile was successfully updated!")
			return redirect('profile')
		#else:
		#	error_message(request,_('Please correct the error below'))
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
	return render(request, 'blog/user_profile.html',{
		'user_form': user_form,
		'profile_form': profile_form,
		})
	user.save()'''

# Create your views here.
def first(request):
	return render(request, 'blog/first_html.html')

'''def register_non_admin_account(request):
	if request.method == 'POST':
		user_non_admin_form = NonAdminAccountForm(request.POST)
		#form = PostForm(request.POST) #temp
		if user_non_admin_form.is_valid():
			user_non_admin_form.save()
			username = user_non_admin_form.cleaned_data.get('username')
			raw_password = user_non_admin_form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		user_non_admin_form = NonAdminAccountForm()
	return render(request, 'registration/register.html', {'user_non_admin_form': user_non_admin_form})'''


def pic_check(request,check,pk):
	user = get_object_or_404(User, pk=pk)
	profile_form = ProfileForm(request.POST or None, request.FILES or None,  instance=user.profile)
	return bool(profile_form.data.get(check, False))

def user_profile(request,pk):
	user = get_object_or_404(User, pk=pk)
	posts = Post.objects.filter(author=pk)
	user_non_admin_form = NonAdminAccountForm(request.POST or None, instance=user)
	
	#if request.method == "POST" and request.FILES['user_cover_pic'] and request.FILES['user_profile_pic']:
	if request.method == "POST":
		profile_form = ProfileForm(request.POST or None, request.FILES or None,  instance=user.profile)
		if profile_form.is_valid() :
			user.profile = profile_form.save(commit=False)
			#user.profile.user_profile_pic = request.FILES['user_profile_pic']
			#user.profile.user_cover_pic = request.FILES['user_cover_pic']
			#user.profile.user_profile_pic = profile_form(request.FILES['user_profile_pic'])
			#user.profile.user_cover_pic = profile_form(request.FILES['user_cover_pic'])

			'''if request.FILES['user_profile_pic'] == '' and request.FILES['user_cover_pic'] == '':
				print("fucking empty and")
			elif request.FILES['user_profile_pic'] == '' or request.FILES['user_cover_pic'] == '':
				print("fucking empty or")
			else:
				user.profile.user_profile_pic = request.FILES['user_profile_pic']
				user.profile.user_cover_pic = request.FILES['user_cover_pic']'''

			if pic_check(request,'user_profile_pic',pk=pk) or pic_check(request,'user_cover_pic',pk=pk):
				print(True)
			else:
				print(False)

			#if profile_form.data['user_profile_pic']:
				#user.profile.user_cover_pic = user.profile.user_cover_pic 
				#user.profile.user_profile_pic = user.profile.user_profile_pic 
				#print('none prof')
			#else:
				#print('not none prof')
				#user.profile.user_profile_pic = request.FILES['user_profile_pic']
				#user.profile.user_cover_pic = request.FILES['user_cover_pic']
			#if 'user_cover_pic' is None :
				#user.profile.user_cover_pic = user.profile.user_cover_pic 
			#	user.profile.user_cover_pic = user.profile.user_cover_pic 
			#	print('none cover')
			#else:
			#	print('not none cover')
			#	user.profile.user_cover_pic = request.FILES['user_cover_pic']
			#name = request.FILES['user_cover_pic'].value()
			#print ("this is cover")
			#print (name)

			user.profile.edited()
			file_type = user.profile.user_profile_pic.url.split('.')[-1]
			file_type2 = user.profile.user_cover_pic.url.split('.')[-1]
			file_type = file_type.lower()
			file_type2 = file_type2.lower()
			if file_type and file_type2 not in IMAGE_FILE_TYPES:
				context = {
					'post': post,
					'form': form,
					'error_message': 'Image file must be PNG, JPG, or JPEG',
				}
				return render(request, 'blog/post_edit.html',context)
			user.profile.save()
			return redirect('profile', pk=user.pk)
	else:
		profile_form = ProfileForm(instance=user.profile)
	context = {
		'user':user,
		'posts': posts,
		'profile_form': profile_form, 
		'user_non_admin_form':user_non_admin_form,
	}
	return render(request, 'blog/user_profile.html', context,)





@login_required
def user_profile_edit(request, pk):
	profile = get_object_or_404(Profile, pk=pk)
	if request.method == "POST":
		profile_form = ProfileForm(request.POST or None,  instance=request.user.profile)
		if profile_form.is_valid():
			profile = profile_form.save(commit=False)
			profile.save()
			return redirect('profile', pk=profile.pk)
	else:
		profile_form = ProfileForm(request.POST or None,  instance=request.user.profile)
	return render(request, 'blog/user_profile_edit.html',{'profile_form': profile_form, 'profile':profile,})


def index(request):
	posts = Post.objects.filter(published_date__lte=timezone.now())
	login_form = LoginForm(prefix='logined')
	user_non_admin_form = NonAdminAccountForm(prefix='registered')
	'''user = get_object_or_404(User, pk=pk)
	profile = get_object_or_404(Profile, pk=pk)
	temp = {
		'posts':posts,
		'user':user,
		'profile': profile,
	}'''

	'''if request.method = "POST":
		#body_vector = SearchVector('posts')
		category_title_vector = SearchVector('posts')
		Post.objects.annotate(search=category_title_search).filter(search='programming')'''

	if request.method == "GET":
		query = request.GET.get("q")
		if query:
			posts = posts.filter(
				Q(title__icontains=query) |
				Q(author__username__icontains=query) |
				Q(text__icontains=query)
				).distinct()
		post_numbers =  posts.count()
	else:
		post_numbers =  posts.count()

	'''list_post_even = []
	list_post_odd = []
	for post in posts.id:
		if post%2==0:
			list_post_even = post
		else:
			list_post_odd = post'''


	#if request.method == 'POST' and request.POST.get("regbtn"):
	if request.method == 'POST':
		if 'regbtn' in request.POST:
			print ("register yo")
			user_non_admin_form = NonAdminAccountForm(request.POST, prefix='registered')
			#form = PostForm(request.POST) #temp
			if user_non_admin_form.is_valid():
				user_non_admin_form.save()
				username = user_non_admin_form.cleaned_data.get('username')
				raw_password = user_non_admin_form.cleaned_data.get('password1')
				user = authenticate(username=username, password=raw_password)
				login(request, user)
				return redirect('index')
		elif 'loginbtn' in request.POST:

			
			print ("login 1")
			login_form = LoginForm(request.POST, prefix='logined')
			#username = request.POST['username']
			#password = request.POST['password']

			#print(username)
			#print(password)
			username = request.POST['logined-username']
			password = request.POST['logined-password1']
			#username = login_form.post('username')
			#password = login_form.post('password1')
			#print (username)
			#print (password)
			print ("login 2")
			#if login_form.is_valid():
			print ("login 3")
				
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				print ("login yo")
			else:
				print("not login")



	else:
		user_non_admin_form = NonAdminAccountForm(prefix='registered')
		login_form = LoginForm( prefix='logined')
		
	#return render(request, 'registration/register.html', {'user_non_admin_form': user_non_admin_form})
	

	context = {
		#'list_post_even':list_post_even,
		#'list_post_odd':list_post_odd, 
		'login_form': login_form,
		'user_non_admin_form': user_non_admin_form,
		'posts': posts,
		'post_numbers': post_numbers
	}
	return render(request, 'blog/index.html', context)



'''def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now())
	return render(request, 'blog/index.html', {'posts': posts})'''

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post_id = post.pk
	liked = False
	if request.session.get('has_liked_'+str(post_id), liked):
		liked = True
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			if request.user.is_authenticated():
				comment.author = request.user.username
				comment.approve()
			else:
				comment.author = "Anonymous"
			comment.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()
	context = {'post': post, 'form': form, 'liked':liked}
	return render(request, 'blog/post_detail.html', context)

'''def hitCountPage(HitCountDetailView):
		post = Post
		count_hit = True'''



def dislike_count_blog(request):
	disliked = False

	if request.method == 'GET':
		post_id = request.GET['post_id']
		post = Post.objects.get(id=int(post_id))
		if request.session.get('has_disliked_'+post_id, disliked):
			print("undislike")
			if post.dislikes > 0:
				dislikes = post.dislikes -1
				try:
					del request.session['has_disliked_'+ post_id]
				except KeyError:
					print("keyerror")
		else:
			print("dislike")
			request.session['has_disliked_'+post_id] = True
			dislikes = post.dislikes + 1
		
	post.dislikes = dislikes
	post.save()
	return HttpResponse(dislikes,disliked)


def like_count_blog(request):
	liked = False

	if request.method == 'GET':
		post_id = request.GET['post_id']
		post = Post.objects.get(id=int(post_id))
		if request.session.get('has_liked_'+post_id, liked):
			print("unlike")
			if post.likes > 0:
				likes = post.likes -1
				try:
					del request.session['has_liked_'+ post_id]
				except KeyError:
					print("keyerror")
		else:
			print("like")
			request.session['has_liked_'+post_id] = True
			likes = post.likes + 1
		
	post.likes = likes
	post.save()
	return HttpResponse(likes,liked)



@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST" :
		form = PostForm(request.POST or None, request.FILES or None, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			
			if pic_check(request,'cover_pic',pk=pk):
				print(True)
			else:
				print(False)

			#post.cover_pic = request.FILES['cover_pic']
			file_type = post.cover_pic.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMAGE_FILE_TYPES:
				context = {
					'post': post,
					'form': form,
					'error_message': 'Image file must be PNG, JPG, or JPEG',
				}
				return render(request, 'blog/post_edit.html',context)
			post.save()
			return redirect('post_detail',pk=post.pk)
	else:
		edit = True
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html',{'form': form,'edit': edit})

@login_required
def post_new(request):
	if request.method == "POST" and request.FILES['cover_pic']:
		form = PostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.cover_pic = request.FILES['cover_pic']
			file_type = post.cover_pic.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMAGE_FILE_TYPES:
				context = {
					'post': post,
					'form': form,
					'error_message': 'Image file must be PNG, JPG, or JPEG',
				}
				return render(request, 'blog/post_edit.html',context)
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)

def publish(self):
    self.published_date = timezone.now()
    self.save()

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

