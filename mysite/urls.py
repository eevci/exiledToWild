from django.conf.urls import patterns, include, url
import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'view.views.index',name="index"),
    url(r'^time/$', 'view.views.current_datetime',name="now"),
    url(r'^map/$', 'view.views.getMap',name="map"),
    url(r'^home/$','view.views.home',name="home"),
    url(r'^sign-up/$','view.views.sign_view',name="sign_view"),
    url(r'^sign-up/signup_post/$','view.views.sign_post',name="sign_post"),
    url(r'^login/$','view.views.login_view',name="login_view"),
    url(r'^login/login_post/$','view.views.login_post',name="login_post"),
    url(r'^logout/$', 'view.views.logout_view', name='logout'),
    url(r'^time/plus/(\d{1,2})/$', 'view.views.hours_ahead',name="hours_ahead"),
    url(r'^image/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^post/form_upload.html$','view.views.post_form_upload', name='post_form_upload'),
)
