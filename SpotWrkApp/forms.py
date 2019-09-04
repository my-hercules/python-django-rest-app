from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms import extras
from datetime import datetime
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.shortcuts import redirect
from SpotWrkApp.models import *

from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic',)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(ProfileForm, self).__init__(*args, **kwargs)
        #self.fields['user']=forms.ModelChoiceField(queryset=UserDefinedCode.objects.filter(owner=user))
        #self.fields['unique_code']=forms.CharField(max_length=15)
"""
class RecprofileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'location', 'skill', 'company_name', 'current_role', 'social_facebook', 'social_linkedin')
        widgets = {
            'first_name':  forms.TextInput(
                attrs={'placeholder': 'First Name', 'required': 'True'}
            ),
            'last_name':  forms.TextInput(
                attrs={'placeholder': 'Last Name', 'required': 'True'}
            ),
            'location': forms.TextInput(
                attrs = {'placeholder':'Location', 'required': 'True'}
            ),
            'skill':   forms.TextInput(
                attrs={'placeholder': 'Skills', 'required': 'True', 'id':'skill'}
            ),
            'company_name':   forms.TextInput(
                attrs={'placeholder': 'Pre filled Company Name', 'required': 'False'}
            ),
            'current_role':   forms.TextInput(
                attrs={'placeholder':'Current Role', 'required' : 'False'}
            ),
            'social_facebook':  forms.TextInput(attrs={
                'required': 'True', 'max_length': '30','render_value': 'False','placeholder':'www.facebook.com/??????'
            }),
            'social_linkedin':  forms.TextInput(attrs={
                'required': 'True', 'max_length': '30', 'render_value': 'False','placeholder':'www.linkedin.com/??????'
            }),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(ProfileForm, self).__init__(*args, **kwargs)
        #self.fields['user']=forms.ModelChoiceField(queryset=UserDefinedCode.objects.filter(owner=user))
        #self.fields['unique_code']=forms.CharField(max_length=15)

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('industry', 'skill', 'location', 'candidate_experience', 'candidate_number')
        widgets = {
            'industry' : forms.Select(
            ),
            'company_name' : forms.TextInput(
                attrs={'placeholder': 'Company Name', 'required': 'True'}
            ),
            'company_description' :forms.Textarea(
                attrs={'placeholder': 'Company description', 'required': 'True'}
            ),
            'company_skill' : forms.TextInput(
                attrs={'placeholder': 'Skills related to your company', 'required': 'True'}
            ),
            'hired_location' : forms.TextInput(
                attrs={'placeholder': 'Locations where you hired most', 'required': 'True'}
            ),
            'company_site'  : forms.TextInput(
                attrs={'placeholder': 'http://yourwebsite.com', 'required': 'True'}
            ),
            'employee_count' : forms.Select(),
        }
"""