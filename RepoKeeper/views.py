from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from models import Recourse
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required
import sys


# Create your views here.
class ManagePage(View):
    @method_decorator(login_required)
    def get(self, request):
        print >> sys.stderr, request.user.id
        context ={'file_list': Recourse.objects.filter(user_id=request.user.id)};
        return render(request, 'RepoKeeper/managePage.html',context)

class Upload(View):
    @method_decorator(login_required)
    def get(self,request):
        pass
    @method_decorator(login_required)
    def post(self, request, *arg, **kwargs):
        file_num = 0;
        if request.FILES and request.FILES.get('upload'):
            res = Recourse()
            res.file= request.FILES.get('upload')
            res.user=request.user
            res.save()
            file_num+=1
            print >> sys.stderr, "save file successed!"
        else:
            print >> sys.stderr, "FILES:" + request.FILES
            print >> sys.stderr, "no file found"
        return HttpResponse("file saved with id:" + str(file_num))