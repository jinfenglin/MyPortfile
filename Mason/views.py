from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
class HomePage(View):
    def get(self, *args):
        return None;