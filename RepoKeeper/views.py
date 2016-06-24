from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from models import Recourse
import sys


# Create your views here.
class ManagePage(View):
    def get(self, request):
        return render(request, 'RepoKeeper/managePage.html')

class Upload(View):
    def post(self, request, *arg, **kwargs):
        video_id = 0;
        if request.FILES and request.FILES.get('upload'):
            res = Recourse()
            res.file = request.FILES.get('upload')
            res.save()
            video_id = res.id
            print >> sys.stderr, "save file successed!"
        else:
            print >> sys.stderr, "FILES:" + request.FILES
            print >> sys.stderr, "no file found"
        return HttpResponse("file saved with id:" + str(video_id))

