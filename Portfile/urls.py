from django.conf.urls import url
from views import *
urlpatterns=[
        url(r'^$',HomePage.as_view(),name='homepage'),
        url(r'^login',Login.as_view(),name='login'),
        url(r'^register',CreateUser.as_view(),name='register'),
        url(r'^activate/(?P<key>.+)$',Activation.as_view(),name='activation'),
        url(r'^resend_activation/(?P<user_id>.+)$',Resend_Activation.as_view(),name='resend'),
]
