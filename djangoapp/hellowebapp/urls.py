"""hellowebapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

#Creating URL links to pages. References to html files

from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
#Django's generic view
from django.views.generic import TemplateView
from collection import views
from collection.views import HomeView, ResultsView
from django.views.generic.base import RedirectView

from collection.modelsfile import Books

#from django.conf.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/',
        TemplateView.as_view(template_name='about.html'),
        name='about'),
    path('contact/',
        TemplateView.as_view(template_name='contact.html'),
        name='contact'),
    path('results/',ResultsView.as_view(), name='results'),
    # path('results/<slug>/', views.result_detail,
    #     name='result_detail'),
    path('admin/', admin.site.urls),
    path('github/',RedirectView.as_view(url='https://github.com/georgetown-analytics/Amazon-Recommenders'),
        name='github'),
]
