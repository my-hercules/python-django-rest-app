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
from django.template.loader import render_to_string, get_template

from django.core.mail import EmailMessage

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.validators import validate_email
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.forms import modelformset_factory
from django.db.models import Q
from django.http import JsonResponse
import json
from django.core import serializers

from employer.models import *
from employer.forms import *
from SpotWrkApp.models import *

from django.forms import BaseModelFormSet


from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError 

def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        from django.utils import simplejson
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')
        

class BaseCandidateFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Ecandidate.objects.none()
class BaseServiceFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BaseServiceFormSet, self).__init__(*args, **kwargs)
        self.user = user
        self.queryset = Service.objects.filter(user = user).all()


def upload_status(request):
    if request.method == 'GET':
        if request.GET['key']:
            if cache.get(request.GET['key']):
                value = cache.get(request.GET['key'])
                return HttpResponse(json.dumps(value), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'error':"No csrf value in cache"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'error':'No parameter key in GET request'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'No GET request'}), content_type="application/json")

def get_dashboard_candidate(request):
	context = {}
	sID = int(request.POST['id'])
	candidate = Ecandidate.objects.get(pk = sID)
	candidateForm = EcandidateForm(instance = candidate)
	context['form'] = candidateForm
	return render_to_response("employer/signup/ajax/ajax_dash_candidate_form.html",context)

def get_dashboard(request):
	context = {}
	user = request.user
	context['user'] = user
	sFrom = request.POST["from"]
	sID = int(request.POST["id"])
	eorder = Eorder.objects.get(pk = sID)
	context['order'] = eorder
	page = "ajax_dash_overview.html"
	candidateform  = EcandidateForm()
	context['form'] = candidateform
	if sFrom == "overview":
		page = "ajax_dash_screening.html"
		
		if eorder.category == "SCREENING":
			if eorder.ecandidate_set.all().count() == 0:
				context['type'] = "File"
			else:
				context['type'] = "Manual"
		else:
			page = "ajax_dash_sourcing.html"
		return render_to_response("employer/signup/ajax/"+page, context)
	return HttpResponse("Error!")

def savePayment(request):
	user = request.user
	try:
		payment = Payment.objects.get(user = user)
	except:
		payment = Payment()
		payment.user = user
		payment.save()
	paymentform = EpaymentForm(request.POST,instance = payment)
	if paymentform.is_valid:
		payment = paymentform.save(commit = False)
		payment.user = user
		payment.save()
	return HttpResponse("success")
def getSearchObject(request):
	s_skill = request.POST['search_skill']
	s_location = request.POST['search_location']
	s_experience = request.POST['search_experience']
	to_show = []
	recruiters = User.objects.filter(is_staff = False)
	for recruiter in recruiters:
		for order in recruiter.tborder_set.all():
			skills = order.skill.split(', ')
			for skill in skills:
				if skill == s_skill:
					to_show.append(recruiter.id)
					break
	if s_skill != '':
		recruiters = User.objects.filter(is_staff = False).filter(id__in = to_show).all()
	
	to_show = []
	for recruiter in recruiters:
		for order in recruiter.tborder_set.all():
			location = order.location
			if location == s_location:
				to_show.append(recruiter.id)
				break
	if s_location != '':
		recruiters = recruiters.filter(id__in = to_show)
	
	to_show = []
	for recruiter in recruiters:
		for order in recruiter.tborder_set.all():
			experience = order.experience
			if experience == s_experience:
				to_show.append(recruiter.id)
				break
	if s_experience != '':
		recruiters = recruiters.filter(id__in = to_show)

	context = {'recruiters':recruiters}
	return render_to_response("employer/signup/ajax/ajax_recruiter_list.html",context)
def getFilterObject(request):
	sFilter = request.GET["filter"]

	to_exclude = []
	filters = sFilter.split(",");
	sub_filters = filters[0].split(":")
	recruiters = User.objects.filter(is_staff = False)
	if filters[0]!="":
		for sub_filter in sub_filters:
			for recruiter in recruiters:
				if sub_filter == "Sourcing":
					category = "SOURCING"
				elif sub_filter == "Screening":
					category = "SCREENING"
				else:
					category = "FULL RECRUITMENT"
				if not recruiter.tborder_set.filter(category = category).exists():
					to_exclude.append(recruiter.id)
	sub_filters = filters[1].split(":")
	if filters[1]!="":
		for sub_filter in sub_filters:
			for recruiter in recruiters:
				if sub_filter == "Percentage":
					fee_type = "%"
				else:
					fee_type = "$"
				if not recruiter.tborder_set.filter(pay_fee_type = fee_type).exists():
					to_exclude.append(recruiter.id)
	sub_filters = filters[2].split(":")
	if filters[2]!="":
		for sub_filter in sub_filters:
			for recruiter in recruiters:
				if sub_filter == "Post pay":
					pay_mode = "POSTPAY"
				else:
					pay_mode = "PREPAY"
				if not recruiter.tborder_set.filter(pay_mode = pay_mode).exists():
					to_exclude.append(recruiter.id)
	sub_filters = filters[3].split(":")
	if filters[3]!="":
		for sub_filter in sub_filters:
			for recruiter in recruiters:
				if sub_filter == "Within 3 days":
					turnaround = "3day"
				elif sub_filter == "Less than a week":
					turnaround = "1week"
				elif sub_filter == "Less than 2 weeks":
					turnaround = "2week"
				elif sub_filter == "Less than 3 weeks":
					turnaround = "3week"
				elif sub_filter == "Less than a month":
					turnaround = "1month"
				if not recruiter.tborder_set.filter(turnaround = turnaround).exists():
					to_exclude.append(recruiter.id)
	recruiters = User.objects.filter(is_staff = False).exclude(id__in = to_exclude).all()
	context = {'recruiters':recruiters}
	return render_to_response("employer/signup/ajax/ajax_recruiter_list.html",context)

def getOrderContent(request):
	data = {}
	context = {}
	order_id = request.GET["order_id"]
	new_order = Tborder.objects.get(pk = int(order_id))
	order_form = EorderForm()
	candidate_form = modelformset_factory(Ecandidate, form=EcandidateForm,extra = 1,formset = BaseCandidateFormSet)
	context['order_form'] = order_form
	context['candidate_form'] = candidate_form
	if new_order.category == "SCREENING":
		data['order_content'] = render_to_string("employer/signup/ajax/ajax_order_screening.html",context)
	else:
		data['order_content'] = render_to_string("employer/signup/ajax/ajax_order_sourcing.html",context)
	data['criteria_origin'] = render_to_string("employer/signup/ajax/ajax_order_criteria.html",{'order':new_order})
	return JsonResponse(data, safe = False)

def newCandidate(request):
	request.GET = request.GET.copy()
	request.GET['form-TOTAL_FORMS'] = int(request.GET['form-TOTAL_FORMS']) + 1

	count = request.GET['candidate_count']
	count = int(count) + 1
	candidate_form = modelformset_factory(Ecandidate, form=EcandidateForm,extra = count)
	candidate_form = candidate_form(request.GET)
	return render_to_response("employer/signup/ajax/ajax_listcandidates.html",{'candidate_form':candidate_form})

def saveProfile(request):
	user = request.user
	profile = Profile.objects.get(user=request.user)
	profileForm = ProfileForm(request.POST, request.FILES,instance = profile)
	if profileForm.is_valid:
		profileForm.save()
	return render_to_response("employer/signup/ajax/ajax_savedprofile.html",{'user':user})

def getProfile(request):
	user = request.user
	profile = Profile.objects.get(user=request.user)
	profileForm = ProfileForm(instance = profile)
	context = {'user':user,'profileform':profileForm}
	return render_to_response("employer/signup/ajax/ajax_editprofile.html",context)

def saveCompany(request):
	user = request.user
	serviceFormSet = modelformset_factory(Service, form=ServiceForm, extra = 0, can_delete=True)
	try:
		company = Company.objects.get(user = user)
		companyForm = CompanyForm(request.POST,instance = company)
	except:
		companyForm = CompanyForm(request.POST)
	if companyForm.is_valid():
		company =  companyForm.save(commit = False)
		company.user = user
		company.save()
	serviceFormSet = serviceFormSet(request.POST)
	if serviceFormSet.is_valid():
		services = serviceFormSet.save(commit = False)
		for service in services:
			service.user = user
			service.save()
	services = user.service_set.all()
	return render_to_response("employer/signup/ajax/ajax_savedcompany.html",{'company':company,'services':services})

def getCompany(request):
	user = request.user
	company = Company.objects.get(user=request.user)
	companyForm = CompanyForm(instance = company)

	serviceFormSet = modelformset_factory(Service, form = ServiceForm, extra=0, formset = BaseServiceFormSet, can_delete = True)
	serviceFormSet = serviceFormSet(user = user)
	#serviceFormSet = modelformset_factory(Service, form=ServiceForm, extra = 0, can_delete = True)
	context = {'user':user,'companyform':companyForm,'serviceformset':serviceFormSet}
	return render_to_response("employer/signup/ajax/ajax_editcompany.html",context)

def newService(request):
	user = request.user
	request.POST = request.POST.copy()
	request.POST['form-TOTAL_FORMS'] = int(request.POST['form-TOTAL_FORMS']) + 1
	serviceFormSet = modelformset_factory(Service, form=ServiceForm, extra = 0, formset = BaseServiceFormSet, can_delete = True)
	serviceformset = serviceFormSet(request.POST,user=user)
	return render_to_response("employer/signup/ajax/ajax_servicelist.html",{'serviceformset':serviceformset})

def deleteService(request):
	user = request.user
	sID = int(request.GET['id'])-1
	request.POST = request.POST.copy()
	form_count = int(request.POST['form-TOTAL_FORMS'])
	#request.POST['form-TOTAL_FORMS'] = form_count
	#for i in range(sID+1,form_count-1):
	request.POST['form-'+str(sID)+'-DELETE'] = 'on'
	#del(request.POST['form-'+str(form_count-1)+'-id'])
	serviceFormSet = modelformset_factory(Service, form=ServiceForm, extra = 0, formset = BaseServiceFormSet, can_delete = True)
	serviceformset = serviceFormSet(request.POST,user = user)
	sServiceID = request.GET['sid']
	if sServiceID != "None":
		sServiceID = int(sServiceID)
		service = Service.objects.get(pk = sServiceID)
		service.delete()
	return render_to_response("employer/signup/ajax/ajax_servicelist.html",{'serviceformset':serviceformset})

def save_profileimage(request):
	user = request.user
	profile = Profile.objects.get(user=request.user)
	profile.profile_pic.delete()
	profileForm = ProfileForm(request.POST, request.FILES,instance = profile)
	if profileForm.is_valid:
		profile = profileForm.save(commit = False)
		#request.FILES['profile_pic'].name = user.id +"."+request.FILES['profile_pic'].name[-3:]
		profile.profile_pic = request.FILES['profile_pic']
		profile.profile_pic.name = str(user.id) +"."+request.FILES['profile_pic'].name[-3:]
		profile.save()
		return HttpResponse(profile.profile_pic.name)
	return HttpResponse("failed")
"""
	Ajax request end
"""
def index(request):
	user = request.user

	if 'user_type' in request.session:
		if user.is_authenticated:
			if request.session['user_type'] == "recruiter" and user.is_staff == False:
				user.is_staff = False
				user.save()
				return HttpResponseRedirect('/home')
	request.session['user_type'] = 'employer'
	if user.is_active:
		return main(request,'profile')
	form = RegistrationForm()
	context = {'form':form}
	if 'status_msg' in request.session:
		context['status_msg'] = request.session['status_msg']
	request.session['status_msg'] = None
	return render_to_response("employer/home/index.html", context)
def main(request,page):
	user = request.user
	context = {}
	list_file = open('static/lists/industry_list.txt', 'r')
	industry_list = list_file.readlines()
	context = {'user':user,'industry_list':industry_list} #,'page':page}
	context['page'] = page
	if page == "dashboard":
		orders = Eorder.objects.filter(employer = user).all()
		context['orders'] = orders
	else:
		profile = Profile.objects.get(user=request.user)
		profileForm = ProfileForm(instance = profile)

		try:
			company = Company.objects.get(user = user)
			companyForm = CompanyForm(instance = company)
		except:
			companyForm = CompanyForm()
		extra = 0
		if user.service_set.count()==0:
			extra = 1
		serviceFormSet = modelformset_factory(Service, form = ServiceForm, extra=extra, formset = BaseServiceFormSet, can_delete = True)
		serviceFormSet = serviceFormSet(user = user)

		recruiters = User.objects.filter(is_staff = False).all()
		page = 'recruiter_list'
		context['recruiters'] = recruiters
		context['profileform'] = profileForm
		context['companyform'] = companyForm
		context['serviceformset'] = serviceFormSet

	return render_to_response("employer/signup/home.html",context)

from django.core.mail import send_mail
def signup(request):
	"""
		User Registration View.
	"""
	if "signup" in request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			user = User.objects.create_user(
				is_staff = True,
				username = email,
				password=form.cleaned_data['password'],
				email=email)
			user.is_active = False
			#g = Group.objects.get(name='employer') 
			#g.user_set.add(user)
			user.save()
			current_site = get_current_site(request)
			"""
				message = render_to_response('acc_activate_employer_email.html', {
				'name':user.email,
				'domain':current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
				})
				mail_subject = 'Activate your blog account.'
				to_email = user.email
				email = EmailMessage(mail_subject, message, to=[to_email])
				email.send()
			"""

			email_data = {
			'name':user.email,
			'domain':current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': account_activation_token.make_token(user),
			}
			t = get_template('acc_activate_employer_email.html')
			content = t.render(email_data)
			to_email = user.email
			msg = EmailMessage('Activate your account', content, to=[to_email])
			msg.content_subtype = "html"
			msg.send()
			#send_mail("Activate", "Activate your Account",'tannai.odin@gmail.com',[to_email], fail_silently=False, html_message=content)
			request.session['status_msg'] = 'Verification message was sent'
		else:
			request.session['status_msg'] = 'User already exist'
	elif "signin" in request.POST:
		password=request.POST["password"]
		email=request.POST["email"]
		if User.objects.filter(email=email,is_staff = True).exists():
			user = User.objects.filter(email=email,is_staff = True)[0]
			if user.is_active:
				authenticate(username=user.username, password=password)
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				login(request,user)
				if user.profile.is_completed == False:
					return HttpResponseRedirect("/employer/home")
				else:
					return hirerecruiter(request)
			else:
				request.session['status_msg'] = 'You have to verify first'
		else:
			request.session['status_msg'] = 'User does not exist'
	return HttpResponseRedirect('/employer/home')
def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = Nones
	if user is not None and account_activation_token.check_token(user, token):
		
		user.is_active = True
		user.save()
		# return redirect('home')
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request,user)
		request.session['status_msg'] = 'Congratulations. Your account has been verified'
	else:
		request.session['status_msg'] = 'Actvation link is invalid'
	return HttpResponseRedirect('/employer/home')

def hirerecruiter(request):
	user = request.user
	context = {}
	page = 'recruiter_list'
	if 'first_in_market' not in request.session:
		context['is_first'] = "Yes"
	else:
		context['is_first'] = "No"
	request.session['first_in_market'] = 'No'
	if request.method == 'POST':
		if 'order_id' in request.POST:
			order_id = request.POST["order_id"]
			order = Tborder.objects.get(pk = order_id)
			context['order_type'] = order.category
			context['order_id'] = order_id
		if 'recruiter_id' in request.POST:
			rec_id = request.POST["recruiter_id"]
			recruiter = User.objects.get(pk = rec_id)
			context['recruiter'] = recruiter
		paymentform = EpaymentForm()
		order_form = EorderForm()
		candidate_form = modelformset_factory(Ecandidate, form=EcandidateForm,extra = 1,formset = BaseCandidateFormSet)

		paymentform = EpaymentForm()

		if 'hire' in request.POST:
			rec_id = request.POST['hire']
			recruiter = User.objects.get(pk = rec_id)
			context['recruiter'] = recruiter
			page = 'recruiter_profile'
			context['order_id'] = recruiter.tborder_set.first().id
		elif 'checkout' in request.POST:
			page = 'checkout'
		elif 'save_screening' in request.POST:
			order_form = EorderForm(request.POST)
			if order_form.is_valid:
				eorder = order_form.save(commit = False)
				rec = User.objects.get(pk = rec_id)
				eorder.rec = rec
				eorder.recruiter_order = order
				eorder.recruiter_id = rec_id
				eorder.category = order.category
				eorder.employer = user
				eorder.save()
			candidate_form = candidate_form(request.POST)
			if candidate_form.is_valid:
				candidates = candidate_form.save(commit = False)
				for candidate in candidates:
					candidate.eorder = eorder
					candidate.save()
			page = 'payment'
		elif 'save_sourcing' in request.POST:
			order_form = EorderForm(request.POST)
			if order_form.is_valid:
				eorder = order_form.save(commit = False)
				rec = User.objects.get(pk = rec_id)
				eorder.rec = rec
				eorder.recruiter_order = order
				eorder.recruiter_id = rec_id
				eorder.category = order.category
				eorder.employer = user
				eorder.save()
			page = 'payment'
		elif 'payment' in request.POST:
			page = 'payment'
		context['order_form'] = order_form
		context['candidate_form'] = candidate_form
		context['paymentform'] = paymentform
	else:
		user.profile.is_completed = True
		user.profile.save()
		page = 'recruiter_list'
		context['sourcing_count'] = Tborder.objects.filter(category = "SOURCING").count()
		context['screening_count'] = Tborder.objects.filter(category = "SCREENING").count()
		context['fullrecruitment_count'] = Tborder.objects.filter(category = "FULL RECRUITMENT").count()
	list_file = open('static/lists/industry_list.txt', 'r')
	industry_list = list_file.readlines()
	recruiters = User.objects.filter(is_staff = False).all()
	context['recruiters'] = recruiters
	context['industry_list'] = industry_list
	context['user'] = user
	context['page'] = page
	return render_to_response("employer/signup/home.html",context)
	
