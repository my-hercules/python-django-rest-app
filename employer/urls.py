
from django.conf.urls import  url, include
from django.contrib.auth import views as auth_views

from employer.views import *

ajax_patterns = [
   url(r'^getsearchobject/$', getSearchObject, name='ajax_getsearchobject'),
	url(r'^filterobject/$', getFilterObject, name='ajax_getfilterobject'),
	url(r'^getordercontent/$', getOrderContent, name='ajax_getordertype'),
	url(r'^newcandidate/$', newCandidate, name='ajax_newcandidate'),
	url(r'^saveprofile/$', saveProfile, name='ajax_saveprofile'),
	url(r'^getprofile/$', getProfile, name='ajax_getprofile'),
	url(r'^savecompany/$', saveCompany, name='ajax_savecompany'),
   url(r'^getcompany/$', getCompany, name='ajax_getcompany'),
	url(r'^newservice/$', newService, name='ajax_newservice'),
   url(r'^deleteservice/$', deleteService, name='ajax_deleteservice'),
   url(r'^savepayment/$', savePayment, name='ajax_savepayment'),
   url(r'^saveprofileimage$', save_profileimage, name = "ajax_saveprofileimage"),
   url(r'^get_dashboard$', get_dashboard, name = "ajax_employer_dashboard"),
   url(r'^get_dashboard_candidate$', get_dashboard_candidate, name = "ajax_get_dash_candidate"),
]

urlpatterns = [
   url(r'^home/$', index, name='employer_home'),
   url(r'^$',index),
   url(r'^signup/$', signup, name='employer_signup'),
   url(r'^main/(?P<page>\w+)/$', main, name='employer_main'),
#When submitted from the profile page.
   url(r'^hirerecruiter/$', hirerecruiter, name='employer_hirerecruiter'),
   url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='employer_activate'),
   url(r'ajax/', include(ajax_patterns)),
]