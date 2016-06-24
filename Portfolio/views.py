from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic.edit import FormView, CreateView
from Portfolio.models import *
from Portfolio.forms import *
from django.utils import timezone
from django.http import HttpResponse
import sys, hashlib, random


# Create your views here.
class HomePage(TemplateView):
    template_name = 'Portfolio/homepage.html'

    def get_context_date(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        return context


class Login(FormView):
    template_name = 'Portfolio/login.html'
    form_class = LoginForm
    success_url = "/portfolio"

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        if user is not None:
            login(self.request, user)
        else:
            pass
        return super(Login, self).form_valid(form)


class CreateUser(FormView):
    template_name = 'Portfolio/create_user.html'
    # model= get_user_model()
    form_class = UserCreationForm
    success_url = 'login'

    # fields=['username','first_name','last_name','email','password','confirm password']
    def form_valid(self, form):
        datas = dict()
        datas['username'] = form.cleaned_data['username']
        datas['email'] = form.cleaned_data['email']
        datas['password'] = form.cleaned_data['password']
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = datas['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        datas['activation_key'] = hashlib.sha1(salt + usernamesalt).hexdigest()

        form.save(datas)
        form.send_confirm_email(datas)
        return super(CreateUser, self).form_valid(form)


class Activation(TemplateView):
    template_name = 'Portfolio/activation.html'

    def get_context_data(self, **kwargs):
        context = super(Activation, self).get_context_data(**kwargs)
        key = kwargs['key']
        activation_expired = False
        already_active = False
        profile = get_object_or_404(Profile, activation_key=key)
        user_id = profile.user.id
        if not profile.user.is_active:
            if timezone.now() > profile.key_expires:
                activation_expired = True
            else:
                profile.user.is_active = True
                profile.user.save()
        else:
            already_active = True
        context['activation_expire'] = activation_expired
        context['already_active'] = already_active
        context['user_id'] = user_id
        return context


class ResendActivation(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *arg, **kwargs):
        user_id = kwargs['user_id']
        data = {}
        form = UserCreationForm()
        print >> sys.stderr, str(request.user.id) + ":" + str(user_id)
        if str(request.user.id) == str(user_id) and not request.user.is_active:
            data['username'] = request.user.username
            data['email'] = request.user.email
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            usernamesalt = data['username']
            if isinstance(usernamesalt, unicode):
                usernamesalt = usernamesalt.encode('utf8')
            data['activation_key'] = hashlib.sha1(salt + usernamesalt).hexdigest()
            profile = Profile.objects.get(user=request.user)
            profile.activation_key = data['activation_key']
            profile.key_expires = datetime.datetime.now() + datetime.timedelta(days=2)
            profile.save()
            print >> sys.stderr, "resend"
            form.send_confirm_email(data)
        else:
            pass
        return redirect('homepage')


class Edit(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'Portfolio/masterpiece_edit.html')

    def post(self, request, *arg, **kwargs):
        video_id = 0;
        if request.FILES and request.FILES.get('upload'):
            video = Video()
            video.video = request.FILES.get('upload')
            video.save()
            video_id = video.id
            print >> sys.stderr, "save file successed!"
        else:
            print >> sys.stderr, "FILES:" + request.FILES
            print >> sys.stderr, "no file found"
        return HttpResponse("file saved with id:" + str(video_id))


class Detail(View):
    def post(self, request, *arg, **kwargs):
        tmp = list()
        tmp.append(request.POST.get('html_element'))
        request.session['test'] = tmp;
        return HttpResponse("detail")

    def get(self, request, *arg, **kwargs):
        print >> sys.stderr, "**********************"
        print >> sys.stderr, request.session['test'];
        context = {'html_element': request.session['test']}
        return render(request, 'Portfolio/masterpiece_detail.html', context)
