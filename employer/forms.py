from django.http import HttpResponseRedirect

from .models import *
#from .models import Uploadfile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms import extras
from datetime import datetime
from django.utils.safestring import mark_safe
from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect
from SpotWrkApp.models import Profile,Payment
import employer.views

class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'required':'True', 'placeholder':'Email', 'max_length':'30','class':'form-control'}
    ), label=_("Email"))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'required':'True', 'placeholder':'Password', 'max_length':'30','class':'form-control','render_value':'False'}
    ), label=_("Password"))
    def clean_email(self):
        try:
            User.objects.get(
                email__iexact=self.cleaned_data['email']
            )
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("The email already used. "
                                      "Please try another one."))

    def clean(self):
        if not self.errors:
            self.cleaned_data['username'] = '%s%s' % (self.cleaned_data['email'].split('@',1)[0], User.objects.count())
        super(RegistrationForm, self).clean()
        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'location', 'skill', 'social_facebook', 'social_linkedin' , 'profile_pic')
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

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('industry', 'company_name', 'company_description', 'company_skill', 'hired_location', 'company_site', 'employee_count')
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
                attrs={'placeholder': 'Locations in where your company hires most', 'required': 'True'}
            ),
            'company_site'  : forms.TextInput(
                attrs={'placeholder': 'http://yourwebsite.com', 'required': 'True', 'value':'http://'}
            ),
            'employee_count' : forms.Select(),
        }
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'description')
        widgets = {
            'name':  forms.TextInput(
                attrs={'placeholder': 'Product/Service', 'required': 'True'}
            ),
            'description': forms.Textarea(attrs={'placeholder': 'Product/Service description', 'required':'True'}),
        }
class EorderForm(forms.ModelForm):
    class Meta:
        model = Eorder
        fields = ('job_detail', 'client_name', 'client_description', 'company_domain', 'needed_skill', 'needed_hours', 'needed_communication')
        widgets = {
            'job_detail':forms.Textarea(
                attrs = {'placeholder':'Describe Job','required':'True'}
            ),
            'client_name':forms.TextInput(
                attrs = {'placeholder':'Client name','required':'True'}
            ),
            'client_description':forms.Textarea(
                attrs = {'placeholder':'Client Description, Product/Service','required':'True'}
            ),
            'company_domain':forms.TextInput(
                attrs = {'placeholder':'http://www.company.com','required':'True','value':'http://'}
            ),
            'needed_skill':forms.TextInput(
                attrs = {'placeholder':'Must go through core skill test','required':'True'}
            ),
            'needed_hours':forms.TextInput(
                attrs = {'placeholder':'Must be willing to work for long hours','required':'True'}
            ),
            'needed_communication':forms.TextInput(
                attrs = {'placeholder':'Must have his communication','required':'True'}
            ),
        }
class EcandidateForm(forms.ModelForm):
    class Meta:
        model = Ecandidate
        fields = ('candidate_fname','candidate_lname','candidate_location','candidate_role','candidate_company','candidate_skill','candidate_email','candidate_phone','candidate_phone','candidate_linkedin','candidate_facebook')
        widgets = {
            'candidate_fname':forms.TextInput(
                attrs = {'placeholder':'First name','required':'False'}
            ),
            'candidate_lname':forms.TextInput(
                attrs = {'placeholder':'Last name','required':'False'}
            ),
            'candidate_location':forms.TextInput(
                attrs = {'placeholder':'Location','required':'False'}
            ),
            'candidate_role':forms.TextInput(
                attrs = {'placeholder':'Current Role','required':'False'}
            ),
            'candidate_company':forms.TextInput(
                attrs = {'placeholder':'Current Company','required':'False'}
            ),
            'candidate_skill':forms.TextInput(
                attrs = {'placeholder':'Skills','required':'False'}
            ),
            'candidate_email':forms.TextInput(
                attrs = {'placeholder':'Email address','required':'False'}
            ),
            'candidate_phone':forms.TextInput(
                attrs = {'placeholder':'Phone','required':'False','onkeypress':'return event.charCode >= 48 && event.charCode <= 57'}
            ),
            'candidate_linkedin':forms.TextInput(
                attrs = {'placeholder':'www.linkedin.com/??????','required':'False'}
            ),
            'candidate_facebook':forms.TextInput(
                attrs = {'placeholder':'www.facebook.com/??????','required':'False'}
            ),
        }
class EpaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('first_name','last_name','address1','address2','zipcode','pay_pal_cardnumber','pay_pal_code','pay_pal_valid','pay_pal_nameoncard','pay_credit_cardnumber','pay_credit_code','pay_credit_valid','pay_credit_nameoncard','pay_debit_cardnumber','pay_debit_code','pay_debit_valid','pay_debit_nameoncard','invitecode','invite_friend')
        widgets = {
            'first_name':forms.TextInput(
                attrs = {'placeholder':'First name','required':'True'}
            ),
            'last_name':forms.TextInput(
                attrs = {'placeholder':'Last name','required':'True'}
            ),
            'address1':forms.TextInput(
                attrs = {'placeholder':'Address Line 1','required':'True'}
            ),
            'address2':forms.TextInput(
                attrs = {'placeholder':'Address Line 2','required':'True'}
            ),
            'zipcode':forms.TextInput(
                attrs = {'placeholder':'ZIPCODE/PINCODE','required':'True'}
            ),
            'invitecode':forms.TextInput(
                attrs = {'placeholder':'Invite Code','required':'True'}
            ),
            'invite_friend':forms.TextInput(
                attrs = {'placeholder':'Invite a friend','required':'True'}
            ),
            'pay_pal_cardnumber':forms.TextInput(
                attrs = {'placeholder':'Card Number',}
            ),
            'pay_pal_code':forms.TextInput(
                attrs = {'placeholder':'code',}
            ),
            'pay_pal_valid':forms.TextInput(
                attrs = {'placeholder':'Valid through MM/YY',}
            ),
            'pay_pal_nameoncard':forms.TextInput(
                attrs = {'placeholder':'Name on card'}
            ),
            'pay_credit_cardnumber':forms.TextInput(
                attrs = {'placeholder':'Card Number',}
            ),
            'pay_credit_code':forms.TextInput(
                attrs = {'placeholder':'code',}
            ),
            'pay_credit_valid':forms.TextInput(
                attrs = {'placeholder':'Valid through MM/YY',}
            ),
            'pay_credit_nameoncard':forms.TextInput(
                attrs = {'placeholder':'Name on card',}
            ),
            'pay_debit_cardnumber':forms.TextInput(
                attrs = {'placeholder':'Card Number',}
            ),
            'pay_debit_code':forms.TextInput(
                attrs = {'placeholder':'code',}
            ),
            'pay_debit_valid':forms.TextInput(
                attrs = {'placeholder':'Valid through MM/YY',}
            ),
            'pay_debit_nameoncard':forms.TextInput(
                attrs = {'placeholder':'Name on card',}
            ),
        }