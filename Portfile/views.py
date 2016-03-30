from django.shortcuts import render
from django.contrib.auth import get_user_model
#from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView,RedirectView,View
from django.views.generic.edit import FormView,CreateView
from Portfile.models import *
from Portfile.forms import *
import sys,hashlib,random

# Create your views here.
class HomePage(TemplateView):
    template_name='Portfile/homepage.html'
    def get_context_date(self,**kwargs):
        context=super(HomePage,self).get_context_data(**kwargs)
        return context
class Login(FormView):
    template_name='Portfile/login.html'
    def get_context_data(self,**kwrags):
        context=super(Login,self).get_context_data(**kwrags)
        return context
class CreateUser(FormView):
    template_name='Portfile/create_user.html'
    #model= get_user_model()
    form_class=UserCreationForm
    success_url='/portfile'
    #fields=['username','first_name','last_name','email','password','confirm password']
    def form_valid(self,form):
        datas={}
        datas['username']=form.cleaned_data['username']
        datas['email']=form.cleaned_data['email']
        datas['password']=form.cleaned_data['password']
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = datas['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

        form.save(datas)
        form.send_confirm_email(datas)
        return super(CreateUser,self).form_valid(form)

class Activation(TemplateView):
    template_view='acitvation.html'
    def get_context_data(self,**kwargs):
        context= super(Activation,self).get_context_data(**kwargs)
        key=kwargs['key']
        activation_expired=False
        already_active=False
        user_id=None
        profile=get_object_or_404(Profile,activation_key=key)
        if profil.user.is_active==False:
            if timezone.now()> profile.key_expires:
               activation_expired=True 
               user_id=profile.user.id
            else:
                profile.user.is_active=True
                profile.user.save()
        else:
            already_active=True
        context['activation_expire']=activation_expired
        context['already_active']=already_active
        context['user_id']=user_id
        return context
class Resend_Activation(View):
    def get(self,request,*arg,**kwargs):
       user_id=kwargs['user_id']
       datas={}
       form=UserCreationForm()
       if request.user.id==user_id and not user.is_active:
           datas['username']=request.user.username
           datas['email']=request.user.email
           salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
           usernamesalt = datas['username']
           if isinstance(usernamesalt, unicode):
               usernamesalt = usernamesalt.encode('utf8')
           datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()
           profile=Profile.objects.get(user=request.user)
           profile.activation_key=datas['activation_key']
           profile.key_expires=datatime.date()+datetime.timedelta(days=2)
           profile.save()
           form.send_confirm_email(datas)
       else:
           pass
       return redirect('/portfile')
        
