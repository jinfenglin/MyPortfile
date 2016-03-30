from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from Portfile.models import *
from django.core.mail import send_mail

class UserCreationForm(forms.Form):
    username=forms.CharField(max_length=20)
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    comfirm_password=forms.CharField(widget=forms.PasswordInput)
    def save(self,datas):
        user=get_user_model().objects.create_user(
                username=datas['username'],
                password=datas['password'],
                email=datas['email']
                )
        user.is_active=False
       
        profile=Profile()
        profile.activation_key=datas['activation_key']
        profile.key_expires=datetime.datetime.now()+datetime.timedelta(days=2)
        user.save()
        profile.save()
 
    def send_confirm_email(self,datas):
        link='localhost:8080:protfile/activate/'+datas['activation_key']
        context=Context({'activation_link':link,'username':datas['username']})
        template=get_template('Portfile/activation_email.html')
        message=template.render(context)
        send_mail(
                'Portfile Activation',
                message,
                'Dont Reply <do_not_replay@mydomain.com>',
                [datas['email']],
                fail_silently=False
                )
        

