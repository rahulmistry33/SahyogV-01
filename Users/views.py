from django.shortcuts import render, redirect
import requests
import json
from django.http import JsonResponse
from django.http import HttpResponse
import datetime
from bson.json_util import dumps
import pymongo
import dns
import os
from dotenv import load_dotenv
from twilio.rest import Client
from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField()
    email = forms.EmailField(required=True, max_length=60)
    phone_number = forms.CharField(required=True, max_length=13)
    home_address = forms.CharField(required=True)
    work_address = forms.CharField(required=True)
    emergency_contact_1 = forms.CharField(required=True, max_length=13)
    emergency_contact_2 = forms.CharField(required=True, max_length=13)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'phone_number',
            'home_address',
            'work_address',
            'emergency_contact_1',
            'emergency_contact_2'
        )

class LoginForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'password')

client = pymongo.MongoClient("mongodb+srv://"+str(os.getenv("USER"))+":"+str(os.getenv("PASSWORD"))+"@devcluster-qbbgy.mongodb.net/Sahyog?retryWrites=true&w=majority")
db = client.Sahyog
locationDB = db.Location
userDB = db.User

# Create your views here.
def SOS(request):
    to = '+919833139713'
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    response = client.messages.create(
    body='Get me a pizza, with extra cheese, and also a burger, and some choco chipss :)', 
    to=to, from_=os.getenv('TWILIO_PHONE_NUMBER'))
    return HttpResponse("hello")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            ec1 = form.cleaned_data["emergency_contact_1"]
            ec2 = form.cleaned_data["emergency_contact_2"]
            user = {
                "username": username, 
                "fname": form.cleaned_data["first_name"],
                "lname": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password2"],
                "phone": form.cleaned_data["phone_number"],
                "home": form.cleaned_data["home_address"],
                "work": form.cleaned_data["work_address"],
                "ec1": ec1,
                "ec2": ec2
            }
            userDB.insert_one(user)
            request.session['username'] = username
            request.session['ec1'] = ec1
            request.session['ec2'] = ec2
            return redirect(dashboard, form.cleaned_data["username"])
    else:
        form = RegisterForm()
    return render(request, 'UserViews/register.html', {"form": form})


def login(request):
    if request.session.has_key('username'):
        return redirect(dashboard, {"username": username})
    else:
        if request.method=="POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                try:
                    username = form.cleaned_data["username"]
                    user = userDB.find_one({"username": username})
                    if user["password"] == form.cleaned_data["password"]:
                        request.session["username"] = username
                        request.session["ec1"] = user["ec1"]
                        request.session["ec2"] = user["ec2"]
                        return redirect(dashboard, username)
                except:
                    return redirect(register)
            else:
                return render(request, 'UserViews/login.html', {"form": form})
        else:
            form = LoginForm()
        return render(request, 'UserViews/login.html', {"form": form})

def dashboard(request, username):
    if request.session.has_key('username'):
        print(request.session['username'])
        print(request.session['ec1'])
        print(request.session['ec2'])
        return render(request, 'UserViews/dashboard.html', {"username": username})
    else: 
        return redirect(index)

def logout(request):
   try:
      request.session.clear()
   except:
      pass
   return redirect(index)

def index(request):
    if request.method == "POST":
        location = request.POST.get('location')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        load_dotenv()
        location = {"lat": lat, "lng": lng, "location": location}
        locationDB.insert_one(location)        
        return HttpResponse(json.dumps({'status':'success','latitude':lat,'longitude':lng}),content_type='application/json')
        
    else:
        if request.session.has_key('username'):
            print(request.session['username'])
        return render(request,'UserViews/user.html')


def random(request):
    locations = dumps(locationDB.find())
    return HttpResponse(
        "data: "+locations+"\n\n",
        content_type='text/event-stream'
    )



# from django.shortcuts import render
# import requests
# import json
# from django.http import JsonResponse
# from django.http import HttpResponse





# # Create your views here.

    

# def index(request):
#     if request.method == "POST":

#         description = request.POST.get('description')
#         location = request.POST.get('location')
#         print("location :",location)
#         URL = "https://geocoder.ls.hereapi.com/6.2/geocode.json?apiKey=jVB385WpgHu9PmsnaQeW2-qVfltkDlccMdda8oicJQs&searchtext={}".format(location)
#         response = requests.get(URL)
#         data = response.json()
#         print(data)
#         print("response isssss:",data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude'])
#         latitude = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude']
#         longitude = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']
        
        
#         return HttpResponse(json.dumps({'status':'success','latitude':latitude,'longitude':longitude}),content_type='application/json')
        
    
#     else:
#         return render(request,'UserViews/user.html')

        
        
       

    
        
#         """print(r['Response']['View'][3]['Location']['DisplayPosition']['Lattitude'])"""
#         """context = {
#             'lat':latitude,
#             'long':longitude
#         }"""
#         """return render(request,'UserViews/user.html',context)"""





