from django.conf.urls import url

from app import views
from app import  views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/', views.about, name='about'),
    url(r'^document/', views.documentation, name='document'),
    url(r'^api/compute', views.compute, name='compute'),
]