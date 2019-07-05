"""pkapps URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin, auth
from django.views.generic import RedirectView
from django_xmlrpc.views import handle_xmlrpc
from . import views

urlpatterns = [
    url(r'^$', views.show_customerlist),
    url(r'^customerlist/$', views.show_customerlist),
    url(r'^customer/(?P<cid>\d+)$', views.show_customer),
    url(r'^ajax/clst_search/$', views.ajax_clst_search),
    url(r'^ajax/note_action/$', views.ajax_note_action),
    url(r'^ajax/change_state/$', views.ajax_change_state),
    url(r'^xmlrpc/$', handle_xmlrpc, name='xmlrpc'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/img/favicon.ico')),
]

