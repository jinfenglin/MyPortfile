from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from models import Recourse
from django.utils.decorators import method_decorator
from django.core import serializers
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import os
import sys


# Create your views here.
class ManagePage(View):
    @method_decorator(login_required)
    def get(self, request):
        file_list = mark_safe(serializers.serialize('json', Recourse.objects.filter(user_id=request.user.id)))
        print >> sys.stderr, request.user.id
        context = {'file_list': file_list};
        return render(request, 'RepoKeeper/managePage.html', context)


class Upload(View):
    TYPE_BOOK = {
        ".pdf": "TEXT",
        ".mp3": "AUDIO",
        ".jpg": "IMAGE",
        ".mp4": "VIDEO"
    }

    def getType(self, path):
        ext = os.path.splitext(path)[1]
        if ext not in self.TYPE_BOOK:
            return "UNKNOWN"
        return self.TYPE_BOOK[ext.lower()]

    @method_decorator(login_required)
    def get(self, request):
        pass

    @method_decorator(login_required)
    def post(self, request, *arg, **kwargs):
        file_num = 0;
        if request.FILES and request.FILES.get('upload'):
            res = Recourse()
            file = request.FILES.get('upload')
            type = self.getType(file.name)
            res.file = file
            res.user = request.user
            res.media_type = type
            res.save()
            file_num += 1
            print >> sys.stderr, "save file successed!", file.name, type
        else:
            print >> sys.stderr, "FILES:" + request.FILES
            print >> sys.stderr, "no file found"
        return HttpResponse("file saved with id:" + str(file_num))
