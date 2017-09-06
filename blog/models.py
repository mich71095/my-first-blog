from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver	


class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=datetime.now, blank=True)
	published_date = models.DateTimeField(blank=True, null=True)
	cover_pic = models.ImageField(upload_to='post/')
	post_description = models.TextField(max_length=500, blank=True)
	likes = models.PositiveIntegerField(default=0)
	dislikes = models.PositiveIntegerField(default=0)

	def publish(self):
		self.published_date = datetime.datetime.now()
		self.save()

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.published_date <= now

	def approved_comments(self):
		return self.comments.filter(approved_comment=True)

	@property
	def total_likes(self):
		return self.likes.count()

	@property
	def total_dislikes(self):
		return self.dislikes.count()

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey('blog.Post', related_name='comments')
	author = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=datetime.now, blank=True)
	approved_comment = models.BooleanField(default=False)

	def approve(self):
		self.approved_comment = True
		self.save()

	def __str__(self):
		return self.text

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_cover_pic = models.ImageField(null=True,upload_to='user/cover/')
	user_profile_pic = models.ImageField(null=True,upload_to='user/profile/')
	location = models.CharField(max_length=30, null=True)
	birth_date = models.DateField(null=True)
	gender = models.CharField(max_length=30, null=True)
	lives = models.CharField(max_length=100, null=True)
	status = models.CharField(max_length=50, null=True)
	followers = models.IntegerField(default=0,null=True)
	following = models.IntegerField(default=0,null=True)
	work = models.CharField(max_length=200, null=True)
	studied = models.CharField(max_length=200, null=True)
	profession = models.CharField(max_length=200, null=True)
	language = models.CharField(max_length=200, null=True)
	motto = models.CharField(max_length=200, null=True)
	about_me = models.TextField(max_length=500, null=True)
	edit_status = models.BooleanField(default=False)
	

	def edited(self):
		self.edit_status = True
		self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
