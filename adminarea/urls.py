from django.urls import path 
from . import views

urlpatterns = [
    path('admindashboard/',views.admindashboard,name='admindashboard'),

    
]