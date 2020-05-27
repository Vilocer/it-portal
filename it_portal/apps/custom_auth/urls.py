from django.urls import path
from django.conf.urls import url, include
from . import views
from allauth import urls as allauth_urls

urlpatterns = [
	path('login/', views.CustomLogin),
	path('signup/', views.CustomSignup),
	path('', include(allauth_urls)),
]