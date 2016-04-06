from django.conf.urls import url
from views import *
from django.conf.urls.static import static
urlpatterns=[
        url(r'^$',HomePage.as_view(),name='homepage'),
        url(r'^login',Login.as_view(),name='login'),
        url(r'^register',CreateUser.as_view(),name='register'),
        url(r'^activate/(?P<key>.+)$',Activation.as_view(),name='activation'),
        url(r'^resend_activation/(?P<user_id>.+)$',Resend_Activation.as_view(),name='resend'),
        url(r'^masterpiece_edit',Edit.as_view(),name='edit'),
        url(r'^masterpiece_detail',Detail.as_view(),name='detail'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
