from django.urls import path 
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('random/', views.random, name='random'),
    path('SOS/', views.SOS, name='SOS'),
    path('home/', views.home,name="home"),
    path('safey/', views.safey,name="safey"),
    path('report/', views.report,name="report")


    
]