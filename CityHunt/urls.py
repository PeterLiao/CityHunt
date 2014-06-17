from django.conf.urls import patterns, include, url
from django.contrib import admin
from LeaderBoard.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', hottest_page),
    url(r'^about/', about_page),
    url(r'^hottest/$', hottest_page),
    url(r'^hottest/(?P<post_id>[0-9]+)/$', post_detail_page),
    url(r'^hottest/user/(?P<user_id>[0-9]+)/$', hottest_logged_page),
    url(r'^login/', login_page),
    url(r'^add/', add_post_page),
    url(r'^comment/add/', add_comment_page),
    url(r'^hottest/like/add', add_post_like_page),
    url(r'^fb/', fb_page),
    url(r'^user/add/', add_user),
)
