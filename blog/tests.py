import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Post
# Create your tests here.

class PostModelTests(TestCase):
	def test_was_published_recently_with_old_question(self):
		time = timezone.now() + datetime.timedelta(days=1, seconds=1)
		old_post = Post(published_date=time)
		self.assertIs(old_post.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_post = Post(published_date=time)
		self.assertIs(recent_post.was_published_recently(), True)



