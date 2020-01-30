from django.urls import path 
from . import views

urlpatterns = [
    
    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('validators/',views.validators,name="validators"),
    path('status/',views.status,name="status"),
    path('predictCrime/',views.predictCrime,name="predictCrime"),
    # path('loadValidators/',views.loadValidators,name="loadalidators")
    
    
    

    
    
    

    
]