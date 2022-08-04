"""onlinebanking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from re import template
from unicodedata import name
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from onlinebanking.staffapp.views import SignUpView
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

# Added the seecond line in the url patterns, empty quote means home page. and templste name is the html file and you can name it anything.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    re_path(r'^profile', TemplateView.as_view(template_name='profile.html'), name="profile"),
    re_path(r'^setting', TemplateView.as_view(template_name='settings.html'), name="settings"),
    re_path(r'^dashboard', TemplateView.as_view(template_name='dashboard.html'), name="dashboard"),
    re_path(r'^about', TemplateView.as_view(template_name='about.html'), name="about"),
    re_path(r'^contact', TemplateView.as_view(template_name='contact.html'), name="contact"),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^accounts/signup/$', SignUpView.as_view(), name= "signup"),
    re_path(r'^staff/', include('onlinebanking.staffapp.urls')),
    re_path(r'^transactions/', include('onlinebanking.transactionapp.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)