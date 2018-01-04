from django.conf.urls import url

from app import views
from app import  views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/', views.apropos, name='apropos'),
    url(r'^document/', views.documentation, name='document'),
]