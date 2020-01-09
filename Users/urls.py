from django.urls import path 
from . import views

urlpatterns = [
    path('landing/',views.landing,name='landing'),
    path('index/',views.index,name='index'),
    

    
]