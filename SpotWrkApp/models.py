from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.forms import forms
from employer.models import *

class Profile(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)

	first_name = models.CharField(max_length = 30, blank = True)
	last_name = models.CharField(max_length = 30, blank = True)
	is_completed = models.BooleanField(default = False)
	location = models.CharField(max_length=30, blank=True)
	skill = models.TextField(blank = True)
	is_company = models.BooleanField(default = False)
	company_name = models.CharField(max_length=30, blank=True)
	current_role = models.CharField(max_length=30, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	profile_pic=models.ImageField(upload_to='static/upload/',default = 'static/img/spotwrk/usericon.png')
	social_linkedin = models.CharField(max_length=30, blank=True)
	social_facebook = models.CharField(max_length=30, blank=True)

	last_access = models.DateField(null=True, blank=True)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile = Profile.objects.create(user=instance)
		if sender.is_staff == True:
			profile.group = "employer"
		else:
			profile.group = "recruiter"
		profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Experience(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	industry = models.CharField(max_length=30,blank=True)
	skill = models.TextField(blank=True)
	location = models.CharField(max_length=30,blank=True)
	candidate_experience = models.CharField(max_length=30, blank=True)
	candidate_number = models.IntegerField(default=1)
	company_number = models.IntegerField(default = 0)
	hired_count = models.IntegerField(default = 0)
	new_flag = models.IntegerField(default = 1)
	def __str__(self):              # __unicode__ on Python 2
	    return self.user
	class Meta:
		ordering = ('-id',)

class Candidate(models.Model):
	experience = models.ForeignKey(Experience)
	description = models.TextField(blank=True)
	client_name = models.CharField(max_length=30,blank=True)
	client_description = models.CharField(max_length=200,blank=True)
	client_site = models.CharField(max_length=100,blank=True)
	new_flag = models.IntegerField(default = 1)
	candidate_JD = models.FileField(db_index=True,upload_to='static/upload/recruiter/JD/',default = 'static/img/spotwrk/usericon.png')
	new_flag = models.IntegerField(default = 0)
	def __str__(self):              # __unicode__ on Python 2
	    return self.client_name
	class Meta:
		ordering = ('new_flag',)
class Candidateinfo(models.Model):
	candidate = models.ForeignKey(Candidate)

	firstname = models.CharField(max_length=30,blank=True)
	lastname = models.CharField(max_length=30,blank=True)
	skills = models.TextField(blank=True)
	social_linkedin = models.TextField(max_length=30,blank=True)
	candidate_resume = models.FileField(db_index=True,upload_to = 'static/upload/recruiter/resume',default = 'static/img/spotwrk/usericon.png')
	
	def __str__(self):
		return self.candidate
	class Meta:
		ordering = ('id',)

class Tborder(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	category = models.CharField(max_length=30,blank=True)
	industry = models.CharField(max_length=30,blank=True)
	skill = models.TextField(blank=True)
	location = models.CharField(max_length=30,blank=True)
	experience = models.CharField(max_length=30,default = "Mid level")
	criteria = models.TextField(blank=True,default = "None")
	criteria_header = models.CharField(max_length=30,blank = True,default = "None")
	pay_mode = models.CharField(max_length=30,blank=True)
	pay_type = models.CharField(max_length=30,blank=True)
	pay_flatfee = models.IntegerField(default=300)
	pay_fee_type = models.CharField(max_length=30,default="$")
	turnaround = models.CharField(max_length=30,blank=True)
	new_flag = models.IntegerField(default = 1)

	def __str__(self):
		return self.user
	class Meta:
		ordering = ('new_flag',)

class Payment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	address1 = models.CharField(max_length=30, blank=True)
	address2 = models.CharField(max_length=30, blank=True)

	country = models.CharField(max_length=30, blank=True)
	city = models.CharField(max_length=30, blank=True)
	state = models.CharField(max_length=30, blank=True)

	zipcode = models.CharField(max_length=30, blank=True)

	pay_pal_cardnumber = models.CharField(max_length=30,default = "",blank = True)
	pay_pal_code = models.CharField(max_length=30,default = "",blank = True)
	pay_pal_valid = models.CharField(max_length=30,default = "",blank = True)
	pay_pal_nameoncard = models.CharField(max_length=30,default = "",blank = True)

	pay_credit_cardnumber = models.CharField(max_length=30,default = "",blank = True)
	pay_credit_code = models.CharField(max_length=30,default = "",blank = True)
	pay_credit_valid = models.CharField(max_length=30,default = "",blank = True)
	pay_credit_nameoncard = models.CharField(max_length=30,default = "",blank = True)

	pay_debit_cardnumber = models.CharField(max_length=30,default = "",blank = True)
	pay_debit_code = models.CharField(max_length=30,default = "",blank = True)
	pay_debit_valid = models.CharField(max_length=30,default = "",blank = True)
	pay_debit_nameoncard = models.CharField(max_length=30,default = "",blank = True)

	invitecode = models.CharField(max_length=30, default = "",blank = True)
	invite_friend = models.CharField(max_length=30, default = "",blank = True)

	def __str__(self):
		return self.user
	class Meta:
		ordering = ('first_name',)