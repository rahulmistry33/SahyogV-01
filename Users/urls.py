from django.urls import path 
from . import views

urlpatterns = [
    path('landing/',views.landing,name='landing'),
    path('emergency/',views.emergency,name='emergency'),
    path('index/',views.index,name='index'),
    

    
]