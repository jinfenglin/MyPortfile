from django.conf.urls import url
from views import *
urlpatterns=[
        url(r'^$',HomePage.as_view(),name='homepage'),
        url(r'^login',Login.as_view(),name='login'),
]
