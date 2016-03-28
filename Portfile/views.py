from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.
class HomePage(TemplateView):
    template_name='Portfile/homepage.html'
    def get_context_date(self,**kwargs):
        context=super(HomePage,self).get_context_data(**kwargs)
        return context
class Login(TemplateView):
    template_name='Portfile/login.html'
    def get_context_data(self,**kwrags):
        context=super(Login,self).get_context_data(**kwrags)
        return context
