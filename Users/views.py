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
import math, random

client = pymongo.MongoClient("mongodb+srv://"+str(os.getenv("USER"))+":"+str(os.getenv("PASSWORD"))+"@devcluster-qbbgy.mongodb.net/Sahyog?retryWrites=true&w=majority")
db = client.Sahyog
locationDB = db.Location
userDB = db.User

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
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control"}))
    class Meta:
        model = User
        fields = ('username', 'password')

def sendSMS(to, body):
    to = to
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    response = client.messages.create(
    body=body, 
    to=to, from_=os.getenv('TWILIO_PHONE_NUMBER'))
    
# @describe: 6-digit random OTP generator function....
def OTPGenerator():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random()*10)]
    return OTP 

# @describe: Send an SOS emergency message to users' emergency contacts....
def SOS(request):
    sendSMS(request.session['ec1'], 'There\'s an emergency with your colleague. He has met with an accident.')
    sendSMS(request.session['ec2'], 'There\'s an emergency with your colleague. He has met with an accident.')
    return HttpResponse("hello")

# @describe: Register new user 
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = {
                "username": form.cleaned_data["username"], 
                "fname": form.cleaned_data["first_name"],
                "lname": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password2"],
                "phone": '+91'+ form.cleaned_data["phone_number"],
                "home": form.cleaned_data["home_address"],
                "work": form.cleaned_data["work_address"],
                "ec1": '+91'+ form.cleaned_data["emergency_contact_1"],
                "ec2": '+91'+ form.cleaned_data["emergency_contact_2"]
            }
            return redirect(validateOTP, json.dumps(user))
    else:
        form = RegisterForm()
    return render(request, 'UserViews/register.html', {"form": form})

# @describe: Verify the OTP sent to newly registered user.....
def validateOTP(request, user):
    user = user.replace("\'","\"")
    userObj = json.loads(user)
    if request.method == "POST":
        otp = request.POST.get('otp')
        if otp == request.session["otp"]:
            userDB.insert_one(userObj)
            request.session['username'] = userObj["username"]
            request.session['ec1'] = userObj["ec1"]
            request.session['ec2'] = userObj["ec2"]
            return redirect(dashboard, request.session["username"])

    request.session["otp"] = OTPGenerator()
    sendSMS(userObj['phone'], ('Your OTP is ', request.session["otp"]))
    return render(request, 'UserViews/OTP.html')
     
# @describe: Existing user login
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
    return render(request, 'UserViews/index.html')

def report(request):
    if request.method == "POST":
        location = request.POST.get('location')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        date = datetime.datetime.now()
        crime_type = "theft"
        severity = "2"
        load_dotenv()
        location = {"lat": lat, "lng": lng, "location": location, "date": date, "type": crime_type, "severity": severity}
        locationDB.insert_one(location)        
        return HttpResponse(json.dumps({'status':'success','latitude':lat,'longitude':lng}),content_type='application/json')
        
    else:
        return render(request,'UserViews/report.html')

# Analyse statistics dashboard...
def analytics(request):
    locations = list(locationDB.find({"severity": "2"}))
    return render(request, 'UserViews/analytics.html', {"total_crimes": len(locations)})

# A function for server sent events.... 
# @describe: Add new markers dynamically on to map, without refreshing page...
def SSE(request):
    locations = dumps(locationDB.find())
    return HttpResponse(
        "data: "+locations+"\n\n",
        content_type='text/event-stream'
    )






