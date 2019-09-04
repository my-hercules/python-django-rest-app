
from django.conf.urls import url, include
from django.contrib import admin
from SpotWrkApp import views
from employer import views as employer_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^ajax/recruiter/save_profile$', views.save_profile, name = "ajax_recruiter_saveprofile"),
    url(r'^ajax/recruiter/get_profile$', views.get_profile, name = "ajax_recruiter_getprofile"),
    url(r'^ajax/recruiter/save_experience$', views.save_experience, name = "ajax_saveexperience"),
    url(r'^ajax/recruiter/get_experience$', views.get_experience, name = "ajax_getexperience"),
    url(r'^ajax/recruiter/delete_experience$', views.delete_experience, name = "ajax_deleteexperience"),
    url(r'^ajax/recruiter/new_experience$', views.new_experience, name = "ajax_newexperience"),
    url(r'^ajax/recruiter/get_dashboard$', views.get_dashboard, name = "ajax_recruiter_dashboard"),
    url(r'^ajax/recruiter/get_dashboard_candidate$', views.get_dashboard_candidate, name = "ajax_recruiter_dash_candidate"),

	url(r'^$', employer_views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', views.home),
    url(r'^signup$', views.signup),
    url(r'^ajax/dashboard$', views.dashboard),
    url(r'^ajax/profile$', views.profile),
    url(r'^ajax/freelance-profile/save$', views.profile_overview),
    url(r'^ajax/freelance-profile/edit$', views.profile_edit),
    url(r'^ajax/get_recruiter$', views.profile_recruiter),
    url(r'^ajax/order/(?P<pID>[0-9]{1,4})/$', views.order),
    url(r'^ajax/order$', views.order_simple),
    url(r'^ajax/candidate/(?P<pID>[0-9]{1,4})/$', views.candidate),
    #Candidate delete Ajax call
    url(r'^ajax/candidate_delete/(?P<pID>[0-9]{1,4})/$', views.candidate_delete),
    #Candidate Edit Ajax call
    url(r'^ajax/candidate_edit/(?P<pID>[0-9]{1,4})/$', views.candidate_edit),
    #On new candidate info button
    url(r'^ajax/new_candidateinfo/(?P<pID>[0-9]{1,4})/$', views.new_candidateinfo),
    #Delete temp candidateinfo
    url(r'^ajax/delete_tempcandinfo/$', views.delete_tempcandinfo),
    #Order delete Ajax Call
    url(r'^ajax/order_delete/(?P<pID>[0-9]{1,4})/$', views.order_delete),
    #Recruiter delete Ajax Call
    url(r'^ajax/recruiter_delete/(?P<pID>[0-9]{1,4})/$', views.recruiter_delete),
    #return order count
    url(r'^ajax/get_order_count/$', views.get_order_count),

    url(r'^ajax/payment$', views.viewpayment),
    url(r'^register/$', views.register),

    url(r'^loginuser/$', views.loginuser),
    url(r'^logout/$', views.logoutuser),

    url(r'^createprofile$', views.createprofile),
    #When save button pressed
    url(r'^createcandidate/(?P<pID>[0-9]{1,4})/$', views.createcandidate),
    #When Add candidate
    url(r'^addcandidate/(?P<pID>[0-9]{1,4})/$', views.addcandidate),
    #get all candidate and candidateinfo
    url(r'^getallcandidate/(?P<pID>[0-9]{1,4})/$', views.getallcandidate),

    url(r'^add_recruiter$', views.add_recruiter),
    #When edit clcked and then create button is clicked
    url(r'^createorder/(?P<pID>[0-9]{1,4})/$', views.createorder),
    #Create a new order
    url(r'^createorder/$', views.createneworder),
    url(r'^createpayment$', views.createpayment),
    url(r'^payment$', views.payment),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^', include('social_django.urls', namespace='social')),

    url(r'^employer/', include('employer.urls')),
]