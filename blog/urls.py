from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^user_profile/$', views.update_profile, name='profile'),
    url(r'^user_profile/(?P<pk>\d+)/$', views.user_profile, name='profile'),
    url(r'^user_profile/(?P<pk>\d+)/edit/$', views.user_profile_edit, name='user_profile_edit'),
    #url(r'^landingPage$', views.post_list, name='post_list'),    user_profile_edit
    #url(r'^register/$', views.register_non_admin_account, name='register_non_admin_account'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^like-blog/$', views.like_count_blog, name='like_count_blog'),
    url(r'^dislike-blog/$', views.dislike_count_blog, name='dislike_count_blog'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^first/$', views.first, name='first_html'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

]