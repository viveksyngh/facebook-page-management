"""facebook_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	url(r'^$', csrf_exempt(TemplateView.as_view(template_name="index.html"))),
    url(r'^login/$', csrf_exempt(TemplateView.as_view(template_name="login.html"))),
    url(r'^register/$', csrf_exempt(TemplateView.as_view(template_name="register.html"))),
    url(r'^page/', include('page.urls'))
	]
