from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_save
from django.dispatch import receiver
import SpotWrkApp

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    list_file = open('static/lists/industry_list.txt', 'r')
    industry_list = list_file.readlines()
    
    INDUSTRY_CHOICES = [(ind[:-1],ind[:-1]) for ind in industry_list]
    COUNT_CHOICES = [("0<10","0<10"),("10<100","10<100"),("100<500","100<500"),("500<1k","10k<50k"),("50k<100k","50k<100k"),("100k<","100k<"),]

    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES,default = "Accounting")
    company_name = models.CharField(max_length=100,blank = True)
    company_description = models.CharField(max_length=1000,blank = True)
    company_skill = models.CharField(max_length=500,blank = True)
    hired_location = models.CharField(max_length=100,blank = True)
    company_site = models.CharField(max_length=50,blank = True)
    employee_count = models.CharField(max_length=50,blank = True,choices = COUNT_CHOICES)

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100, blank = True)
    description = models.TextField(blank = True)
class Eorder(models.Model):
    employer = models.ForeignKey(User, on_delete = models.CASCADE)
    rec = models.ForeignKey(User, related_name='recruiter_id', null = True)
    recruiter_order = models.ForeignKey('SpotWrkApp.Tborder',on_delete = models.CASCADE,null = True)
    recruiter_id = models.IntegerField(default = -1)
    category = models.CharField(max_length=1000,blank = True)
    job_detail = models.CharField(max_length = 500, blank = True)
    file_JD = models.FileField(upload_to = 'static/upload/employer/JD/')
    client_name = models.CharField(max_length = 500, blank = True)
    client_description = models.TextField(blank = True)
    company_domain = models.CharField(max_length = 500, blank = True)
    needed_skill = models.CharField(max_length = 500, blank = True)
    needed_hours = models.CharField(max_length = 500, blank = True)
    needed_communication = models.CharField(max_length = 500, blank = True)

class Ecandidate(models.Model):
    eorder = models.ForeignKey(Eorder, on_delete = models.CASCADE)
    file_candidate = models.FileField(upload_to = 'static/upload/employer/resume/')
    candidate_fname = models.CharField(max_length = 500, blank = True)
    candidate_lname = models.CharField(max_length = 500, blank = True)
    candidate_location = models.CharField(max_length = 500, blank = True)
    candidate_role = models.CharField(max_length = 500, blank = True)
    candidate_company = models.CharField(max_length = 500, blank = True)
    candidate_skill = models.CharField(max_length = 500, blank = True)
    candidate_email = models.CharField(max_length = 500, blank = True)
    candidate_phone = models.IntegerField(blank = True)
    candidate_linkedin = models.CharField(max_length = 500, blank = True)
    candidate_facebook = models.CharField(max_length = 500, blank = True)