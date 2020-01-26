from django.urls import path
from . import views

urlpatterns = [
#gayatri

	path('index/',views.index, name='index'),
    path('report/',views.report, name='report'),
    path('SSE/', views.SSE, name='SSE'),
    path('SOS/', views.SOS, name='SOS'),
    path('register/', views.register, name='register'),
    # path('dashboard/<username>', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('analytics/', views.analytics, name='analytics'),
    path('validateOTP/<user>', views.validateOTP, name='validateOTP'),
#my addtns
    path('landing/',views.landing,name='landing'),
    path('emergency/',views.emergency,name='emergency'),
# amisha
    #path('index/',views.index,name='index'),
    # path('random/', views.random, name='random'),
    #path('SOS/', views.SOS, name='SOS'),
    path('home/<username>', views.home,name="home"),
    path('safey/', views.safey,name="safey"),
    path('report/', views.report,name="report"),
    path('reportCrime/', views.reportCrime,name="reportCrime")


    

]