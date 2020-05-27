"""it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.user import urls as user_urls
from apps.custom_auth import views as custom_views
from apps.custom_auth import urls as custom_urls
from apps.portal import urls as portal_urls
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('accounts/', include(custom_urls)),
    path('admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),
    path('profile/', include(user_urls)),
    path('', include(portal_urls)),
    path('logout/', custom_views.CustomLogout),
    path('tinymce/', include('tinymce.urls')),
    path('', include('social_django.urls', namespace='social')) 
    

] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
