from django.shortcuts import render, render_to_response, redirect
from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout ,login
from django.http import HttpResponse
from django.core.mail import send_mail

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


from django.core.validators import validate_email

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from SpotWrkApp.models import *
from employer.models import *
from SpotWrkApp.forms import *
#from employer.forms import ProfileForm

from django.contrib.auth.hashers import check_password
from django.core.files.uploadhandler import FileUploadHandler,    UploadFileException   

import json
from django.core.cache import cache
"""
	Ajax process
"""

def save_profile(request):
	context = {}
	user = request.user
	user.profile.first_name = request.POST['first_name']
	user.profile.last_name = request.POST['last_name']
	user.profile.location = request.POST['location']
	user.profile.skill = request.POST['skill']
	if user.profile.is_company:
		user.profile.company_name = request.POST['company_name']
		user.profile.current_role = request.POST['current_role']
	user.profile.social_linkedin = request.POST['linkedin_address']
	user.profile.social_facebook = request.POST['facebook_address']
	user.save()
	context['user'] = user
	return render_to_response("signup/ajax/freelance-profile-overview.html",context)
def get_profile(request):
	context = {}
	user = request.user
	context['user'] = user
	return render_to_response("signup/ajax/freelance-profile-edit.html",context)
def save_experience(request):
	user = request.user
	sID = int(request.POST['exp_id'])
	experience = Experience.objects.get(pk = sID)
	experience.industry = request.POST['industry']
	experience.skill = request.POST['skill']
	experience.location = request.POST['location']
	experience.candidate_experience = request.POST['experience']
	experience.candidate_number = request.POST['count']
	experience.save()
	context = {'exp':experience}
	return render_to_response("signup/ajax/ajax_experience_saved.html",context)
def get_experience(request):
	context = {}
	list_file = open('static/lists/industry_list.txt', 'r')
	industry_list = list_file.readlines()
	sID = int(request.POST['exp_id'])
	experience = Experience.objects.get(pk = sID)
	context['exp']=experience
	context['industry_list'] = industry_list
	return render_to_response("signup/content/recruiter.html",context)
def delete_experience(request):
	sID = int(request.POST['exp_id'])
	experience = Experience.objects.get(pk = sID)
	experience.delete()
	return HttpResponse("success")
def new_experience(request):
	user = request.user
	list_file = open('static/lists/industry_list.txt', 'r')
	industry_list = list_file.readlines()
	experience = Experience()
	experience.user = user
	experience.save()
	sID = experience.id
	data = "<div id = 'experience_form_"+str(sID)+"'>"
	data = data + render_to_string("signup/content/recruiter.html",{'exp':experience,'industry_list':industry_list})
	data = data + "</div>"
	return HttpResponse(data)

def get_dashboard_candidate(request):
	context = {}
	sID = int(request.POST['id'])
	candidate = Ecandidate.objects.get(pk = sID)
	context['candidate'] = candidate
	return render_to_response("signup/ajax/ajax_dash_candidate_form.html",context)

def get_dashboard(request):
	context = {}
	user = request.user
	context['user'] = user
	sFrom = request.POST["from"]
	sID = int(request.POST["id"])
	eorder = Eorder.objects.get(pk = sID)
	context['order'] = eorder
	page = "ajax_dash_overview.html"
	candidate = eorder.ecandidate_set.all().first()
	context['candidate'] = candidate
	if sFrom == "overview":
		page = "ajax_dash_screening.html"
		
		if eorder.category == "SCREENING":
			if eorder.ecandidate_set.all().count() == 0:
				context['type'] = "File"
			else:
				context['type'] = "Manual"
		else:
			page = "ajax_dash_sourcing.html"
		return render_to_response("signup/ajax/"+page, context)
	return HttpResponse("Error!")
"""
	Ajax end
"""

def index(request):
	user = request.user
	request.session['user_type'] = 'recruiter'
	return HttpResponseRedirect('home')
def logoutuser(request):
	logout(request)
	return HttpResponseRedirect('/home')
def loginuser(request):
	myemail = request.POST['txtemail']
	mypassword = request.POST['txtpassword']
	try:
		if User.objects.filter(email = myemail,is_staff = 0).count() == 0:
			request.session['status_msg'] = 'User does not exist!'
			return HttpResponseRedirect('/home')
		user = User.objects.filter(email = myemail,is_staff = False).first()
		if check_password(mypassword, user.password):
			if user.is_active is True:
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				login(request,user)
				if user.profile.is_completed:
					return dashboard(request)
				return signup(request)
			else:
				request.session['status_msg'] = 'You have to verify first'
		else:
			request.session['status_msg'] = 'Password is incorrect'
	except IOError:
		request.session['status_msg'] = 'User does not exist!'
	return HttpResponseRedirect('/home')

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		
		user.is_active = True
		user.save()
		# return redirect('home')
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request,user)
		return signup(request)
	else:
		request.session['status_msg'] = 'Activation link invalid!'
	return HttpResponseRedirect('/home')

def register(request):
	companyname = request.POST['txtcompanyname']
	myemail = request.POST['txtemail']
	password = request.POST['txtpassword']
	if User.objects.filter(username = myemail).count() == 0:
		User.objects.create_user(email = myemail, username = myemail, password = password, is_active = False)
	user = User.objects.filter(username = myemail).first()
	user.email = myemail
	user.set_password(password)

	if user.is_active == True:
		request.session['status_msg'] = 'User already exist!'
		return HttpResponseRedirect('/home')
	user.profile.is_company = False
	if companyname != "":
		user.profile.is_company = True
		user.profile.company_name = companyname
	user.is_active = False
	user.profile.is_completed = False
	user.save()
	current_site = get_current_site(request)
	message = render_to_string('acc_active_email.html', {
	'user':user, 
	'domain':current_site.domain,
	'uid': urlsafe_base64_encode(force_bytes(user.pk)),
	'token': account_activation_token.make_token(user),
	})
	mail_subject = 'Activate your blog account.'
	to_email = myemail
	email = EmailMessage(mail_subject, message, to=[to_email])
	email.send()			

	request.session['status_msg'] = 'Activation email was sent to your email!'
	return HttpResponseRedirect('/home')

def home(request):
	user = request.user
	if user.is_authenticated:
		return HttpResponseRedirect("/signup")
	context = {}
	if 'status_msg' in request.session:
		context['status_msg'] = request.session['status_msg']
	request.session['status_msg'] = None
	context['user'] = user
	return render(request,"home/home.html",context)
def signup(request):
	user = request.user
	list_file = open('static/lists/industry_list.txt', 'r')
	industry_list = list_file.readlines()
	for experience in user.experience_set.all():
		experience.company_number = experience.candidate_set.all().count()
		hired_count = 0
		for candidate in experience.candidate_set.all():
			hired_count = hired_count + candidate.candidateinfo_set.all().count()
		experience.hired_count = hired_count
		experience.save()
	if user.experience_set.all().count()==0:
		experience = Experience()
		experience.user = user
		experience.new_flag = 1
		experience.save()
	profile = Profile.objects.get(user=request.user)
	profileForm = ProfileForm(instance = profile)
	return render_to_response('signup/home.html',{'user' : user,'industry_list':industry_list, 'experience' : user.experience_set.all(),'orders' : user.tborder_set.all(),'page':'signup/content/profile.html','profileform':profileForm})
"""
	cities = City.objects.all()
	f = open( 'static/lists/newlocation.txt', 'w+')
	for city in cities:
		f.write(city.name_ascii)
		f.write(",")
		f.write(city.region.name_ascii)
		f.write("\n")
	f.close()
"""
def dashboard(request):
	user = request.user
	context = {}
	orders = Eorder.objects.filter(rec = user).all()
	context['orders'] = orders
	context['user'] = user
	context['page'] = 'signup/content/dashboard.html'
	return render_to_response('signup/home.html',context)
def viewpayment(request):
	user = request.user
	return render_to_response('signup/home.html',{'user':user,'page':'signup/content/payment.html'})
def profile(request):	
	user = request.user
	if user.experience_set.count() == 0:
		experience = Experience()
		experience.user = user
		experience.new_flag = 1
		experience.save()
	return signup(request)
	return render_to_response('signup/home.html',{'user' : user, 'experience' : user.experience_set.all(),'page':'signup/content/profile.html'})

#This is called when click the edit button on order overview
def order(request,pID):
	user = request.user
	if Tborder.objects.filter(new_flag=0).count() != 0:
		Tborder.objects.filter(new_flag=0)[0].new_flag = 1
	order = Tborder.objects.filter(id=pID)[0]
	order.new_flag = 0
	order.save()
	return HttpResponseRedirect("/ajax/order")
	return render_to_response('signup/home.html',{'user' : user, 'orders' : user.tborder_set.all(),'page':'signup/content/order.html','order':order})
def order_simple(request):
	user = request.user
	order = None
	if user.tborder_set.filter(new_flag = 0).count() != 0:
		order = user.tborder_set.filter(new_flag=0)[0]
	count = user.tborder_set.all().count()

	list_file = open('static/lists/industry_list.txt', 'r')
	industry_list = list_file.readlines()

	return render_to_response('signup/home.html',{'industry_list':industry_list,'user' : user,'count':count, 'order':order, 'orders' : user.tborder_set.all(),'page':'signup/content/order.html'})
def candidate(request,pID):
	user = request.user
	experience = user.experience_set.filter(id=pID)[0]
	candi_edit = experience.candidate_set.filter(new_flag = 1).first()
	if experience.candidate_set.filter(new_flag=1).count()==0:
		candi_edit = Candidate()
		candi_edit.experience = experience
		candi_edit.new_flag = 1
		candi_edit.save()
		candidateinfo = Candidateinfo()
		candidateinfo.candidate = candi_edit
		candidateinfo.save()
	return render_to_response('signup/home.html',{'user':user,'experience':experience,'candidateinfos':candi_edit.candidateinfo_set.all(),'candi_edit':candi_edit, 'candidates':experience.candidate_set.all(), 'page':'signup/content/candidate.html'})
def createprofile(request):
	user = request.user
	if "save_recruiter" in request.POST:
		sID = request.POST["recruiter_saveid"]
		experience = user.experience_set.filter(id = sID)[0]
		experience.industry = request.POST["experience["+sID+"][industry]"]
		experience.skill = request.POST["experience["+sID+"][hire_skill]"]
		experience.location = request.POST["experience["+sID+"][hire_location]"]
		experience.candidate_experience = request.POST["experience["+sID+"][candidate_experience]"]
		experience.candidate_number = request.POST["experience["+sID+"][candidate_count]"]
		experience.user = user
		experience.save()
		return HttpResponseRedirect("/signup")
	user.first_name = request.POST["first_name"]
	user.last_name = request.POST["last_name"]
	user.profile.skill = request.POST["skill"]
	user.profile.location = request.POST["location"]
	user.profile.social_facebook = request.POST["facebook_address"]
	#user.profile.is_completed = True
	user.save()
	if "save" in request.POST:
		if request.POST["facebook_address"] == "":
			user.profile.social_facebook = "None"
		user.profile.social_linkedin = request.POST["linkedin_address"]
		if request.POST["linkedin_address"] == "":
			user.profile.social_linkedin = "None"
		if user.profile.is_company == True:
			user.profile.company_name = request.POST["company_name"]
			user.profile.current_role = request.POST["current_role"]
		return HttpResponseRedirect("/signup")
	i=0
	for experience in user.experience_set.all()	:
		experience.industry = request.POST["experience["+str(experience.id)+"][industry]"]
		experience.skill = request.POST["experience["+str(experience.id)+"][hire_skill]"]
		experience.location = request.POST["experience["+str(experience.id)+"][hire_location]"]
		experience.candidate_experience = request.POST["experience["+str(experience.id)+"][candidate_experience]"]
		experience.candidate_number = request.POST["experience["+str(experience.id)+"][candidate_count]"]
		experience.user = user
		experience.save()
	if "final_submit" in request.POST:
		return HttpResponseRedirect("/ajax/order")
	else:
		return HttpResponseRedirect("/ajax/candidate/"+request.POST["candidate_recid"])
	return render_to_response('signup/home.html',{'user' : user,  'orders' : user.tborder_set.all(),'page':'signup/content/order.html'})
def add_recruiter(request):
	user = request.user
	if user.experience_set.count()==1:
		if user.experience_set.all()[0].new_flag == 1:
			user.experience_set.all()[0].new_flag = 0
	experience = Experience()
	experience.user = user
	experience.new_flag = 1
	experience.save()
	return HttpResponseRedirect("ajax/profile")
	return render_to_response('signup/home.html',{'user':user, 'experience' : user.experience_set.all(),'page':'signup/content/profile.html'})
#get all candidate and candidateinfo
def getallcandidate(request,pID):
	user = request.user
	experience = user.experience_set.filter(id = pID)[0]
	candidates = experience.candidate_set.all()

	saved_part = render_to_response("signup/ajax/get_candidate.html",{'candidates':candidates})
	return HttpResponse(saved_part)
def createcandidate(request,pID):
	user = request.user
	experience = user.experience_set.filter(id = pID)[0]
	
	if(request.POST["candi_id"]!=""):
		candidate = Candidate.objects.filter(id = request.POST["candi_id"])[0]
	else:
		candidate = Candidate()
		candidate.experience = experience
	
	candidate.description = request.POST["skill"]

	candidate.client_name = request.POST["client_name"]
	candidate.client_description = request.POST["client_description"]
	candidate.client_site = request.POST["client_site"]

	candidate.candidate_JD.delete()
	if 'file_JD' in request.FILES:
		candidate.candidate_JD = request.FILES['file_JD']
		candidate.candidate_JD.name = str(candidate.id) +"."+request.FILES['file_JD'].name

	candidate.save()

	candidate.candidateinfo_set.all().delete()
	ran = int(request.POST["candidateinfo_count"])+1

	for i in range(0,ran):
		candidateinfo = Candidateinfo()
		candidateinfo.candidate=candidate
		candidateinfo.firstname = request.POST["candidate_f_name"+str(i)]
		candidateinfo.lastname = request.POST["candidate_l_name"+str(i)]
		candidateinfo.skills = request.POST["candidate_skills"+str(i)]
		candidateinfo.social_linkedin = request.POST["candidate_social_linkedin"+str(i)]
		candidateinfo.save()
		if "candidate_resume"+str(i) in request.FILES:
			candidateinfo.candidate_resume.delete()
			candidateinfo.candidate_resume = request.FILES["candidate_resume"+str(i)]
			candidateinfo.candidate_resume.name = str(candidateinfo.id) +"."+request.FILES["candidate_resume"+str(i)].name
		candidateinfo.save()
	return getallcandidate(request,pID)

def addcandidate(request,pID):
	return HttpResponseRedirect("/ajax/candidate/"+Candidate.objects.filter(id = pID).first().experience.id)
def candidate_delete(request,pID):
	Candidate.objects.filter(id=pID).delete()
	return HttpResponse("Success")
#delete temp candidateinfo
def delete_tempcandinfo(request):
	candidate = Candidate.objects.filter(new_flag = 1).first()
	candidate.delete()
	return HttpResponse("Success")
#On new_candidateinfo
def new_candidateinfo(request,pID):
	candidateinfo = Candidateinfo()
	candidateinfo.candidate = Candidate.objects.filter(id = pID).first()
	candidateinfo.save()
	return render_to_response('signup/ajax/new-candidate.html',{'candidateinfo':candidateinfo})
def candidate_edit(request,pID):
	user = request.user
	candidate = Candidate.objects.filter(id=pID)[0]
	loop = ""

	for i in range(candidate.candidateinfo_set.count(),10):
		loop = loop + str(i)
	data = render_to_response('signup/ajax/edit_candidate.html',{'loop':loop,'candidateinfos':candidate.candidateinfo_set.all(), 'candi_edit':candidate})
	return HttpResponse(data)
#returns order count (ajax call)
def get_order_count(request):
	user = request.user
	if user.tborder_set.all().count()>=2:
		return HttpResponse("success")
	return HttpResponse("failed")
def order_delete(request,pID):
	Tborder.objects.filter(id=pID).delete()
	return HttpResponse(Tborder.objects.all().count())
def recruiter_delete(request,pID):
	user = request.user
	experience = Experience.objects.filter(id=pID).delete()
	return render_to_response('signup/home.html',{'user':user, 'experience' : user.experience_set.all(),'page':'signup/content/profile.html'})

def createorder(request,pID):
	user = request.user
	i = 0
	if Tborder.objects.filter(id = pID).count() != 0:
		Tborder.objects.filter(id = pID)[0].delete()
	order = Tborder()
	order.category = request.POST["order["+str(i)+"][category]"]
	order.industry = request.POST["order["+str(i)+"][industry]"]
	order.skill = request.POST["order["+str(i)+"][order_skill]"]
	order.location = request.POST["order["+str(i)+"][order_location]"]
	order.experience = request.POST["order["+str(i)+"][experience]"]
	order.criteria = request.POST["order["+str(i)+"][criteria]"]
	order.criteria_header = request.POST["order["+str(i)+"][criteria_header]"]
	order.pay_mode = request.POST["order["+str(i)+"][pay_mode]"]
	order.pay_type = request.POST["order["+str(i)+"][pay_type]"]
	order.pay_flatfee = request.POST["order["+str(i)+"][pay_flatfee]"]
	order.turnaround = request.POST["order["+str(i)+"][turnaround]"]
	order.pay_fee_type = request.POST["fee_type"]
	order.user = user
	order.new_flag = 1
	order.save()
	return HttpResponseRedirect("/ajax/order")
	return render_to_response('signup/home.html',{'user' : user, 'orders':user.tborder_set.all(),'page':'signup/content/order.html'})
def createneworder(request):
	user = request.user
	i = 0
	order = Tborder()
	order.category = request.POST["order["+str(i)+"][category]"]
	order.industry = request.POST["order["+str(i)+"][industry]"]
	order.skill = request.POST["order["+str(i)+"][order_skill]"]
	order.location = request.POST["order["+str(i)+"][order_location]"]
	order.experience = request.POST["order["+str(i)+"][experience]"]
	order.criteria = request.POST["order["+str(i)+"][criteria]"]
	order.criteria_header = request.POST["order["+str(i)+"][criteria_header]"]
	order.pay_mode = request.POST["order["+str(i)+"][pay_mode]"]
	order.pay_type = request.POST["order["+str(i)+"][pay_type]"]
	order.pay_flatfee = request.POST["order["+str(i)+"][pay_flatfee]"]
	order.turnaround = request.POST["order["+str(i)+"][turnaround]"]
	order.pay_fee_type = request.POST["fee_type"]
	order.user = user
	order.new_flag = 1
	order.save()
	return HttpResponseRedirect("/ajax/order")
def createpayment(request):
	user = request.user
	payment = user.payment_set.all().first()
	if payment is None:
		payment = Payment()
	payment.first_name = request.POST["first_name"]
	payment.last_name = request.POST["last_name"]
	payment.address1 = request.POST["address1"]
	payment.address2 = request.POST["address2"]
	payment.country = request.POST["country"]
	payment.city = request.POST["city"]
	payment.state = request.POST["state"]
	payment.zipcode = request.POST["zipcode"]

	payment.pay_pal_cardnumber = request.POST["pay_pal_cardnumber"]
	payment.pay_pal_code = request.POST["pay_pal_code"]
	payment.pay_pal_valid = request.POST["pay_pal_code"]
	payment.pay_pal_nameoncard = request.POST["pay_pal_nameoncard"]

	payment.pay_credit_cardnumber = request.POST["pay_credit_cardnumber"]
	payment.pay_credit_code = request.POST["pay_credit_code"]
	payment.pay_credit_valid = request.POST["pay_credit_code"]
	payment.pay_credit_nameoncard = request.POST["pay_credit_nameoncard"]

	payment.pay_debit_cardnumber = request.POST["pay_debit_cardnumber"]
	payment.pay_debit_code = request.POST["pay_debit_code"]
	payment.pay_debit_valid = request.POST["pay_debit_code"]
	payment.pay_debit_nameoncard = request.POST["pay_debit_nameoncard"]

	payment.invitecode = request.POST["invitecode"]
	payment.invite_friend = request.POST["invitefriend"]
	payment.user = user
	payment.save()
	user.profile.is_completed = True
	user.profile.save()
	return dashboard(request)

def payment(request):
	user = request.user
	if(user.payment_set.all().count != 0):
		payment = user.payment_set.all().first()
	else:
		payment = Payment()
		payment.user = user
		payment.save()
	list_file = open('static/lists/locations.txt', 'r')
	cities = list_file.readlines()
	return render_to_response('signup/home.html',{'user' : user, 'payment':payment,'page':'signup/content/payment.html','cities':cities})
def profile_edit(request):
	user = request.user
	return render_to_response('signup/ajax/freelance-profile-edit.html',{'user' : user, 'experience' : user.experience_set.all()})
def profile_overview(request):
	user = request.user
	return render_to_response('signup/ajax/freelance-profile-overview.html',{'user' : user, 'experience' : user.experience_set.all()})
def profile_recruiter(request):
	return render(request,'signup/content/recruiter.html')