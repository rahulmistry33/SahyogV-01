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
    if request.session.has_key('username'):
        sendSMS(request.session['ec1'], 'This is to inform you that your ward/friend is in danger and awaits your help. Access their location using the following link '+'http://www.google.com/maps/place/19.0729578,72.8999708')
        sendSMS(request.session['ec2'], 'This is to inform you that your ward/friend is in danger and awaits your help. Access their location using the following link '+'http://www.google.com/maps/place/19.0729578,72.8999708')
        return render(request, 'UserViews/SOS.html')
    return HttpResponse("hello")


# def index(request):
    # if request.method == "POST":
    #     location = request.POST.get('location')
    #     lat = request.POST.get('lat')
    #     lng = request.POST.get('lng')
    #     crimeType = request.POST.get('crimeType')
    #     crimeLevel = request.POST.get('crimeLevel')
    #     crimeDetails = request.POST.get('crimeDetails')
    #     #print("lat :",lat,"lng :",lng)
    #     #print('location: ',location)
    #     load_dotenv()
    #     location = {"lat": lat, "lng": lng, "location": location, "crimeType":crimeType,"crimeLevel":crimeLevel,"crimeDetails":crimeDetails}
    #     print(location)
    #     users.insert_one(location)        
    #     return HttpResponse(json.dumps({'status':'success','latitude':lat,'longitude':lng}),content_type='application/json')
        

    # else:
    #     return render(request, 'UserViews/index.html')




def getstart(request):
    return render(request,'UserViews/getstart.html')




def safey(request):
    if request.session.has_key('username'):
        return render(request, 'UserViews/safey.html')
    else:
        return render(request,'UserViews/newindex.html')

def report(request):
    if request.session.has_key('username'):
        return render(request, 'UserViews/report.html')
    else:
        return render(request,'UserViews/newindex.html')



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
        if request.session.has_key('username'):
            return home(request,request.session['username'])
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
            return redirect(home, request.session["username"])

    request.session["otp"] = OTPGenerator()
    msg = 'Your OTP is '+request.session['otp']
    sendSMS(userObj['phone'],msg)    
    return render(request, 'UserViews/OTP.html')
     
# @describe: Existing user login
def login(request):
    if request.session.has_key('username'):
        return redirect(home, {"username": request.session['username']})
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
                        return redirect(home, username)
                except:
                    return redirect(register)
            else:
                return render(request, 'UserViews/login.html', {"form": form})
        else:
            form = LoginForm()
        return render(request, 'UserViews/login.html', {"form": form})

def home(request, username):
    if request.session.has_key('username'):
        return render(request, 'UserViews/home.html', {"username": username})
    else: 
        return redirect(index)

def logout(request):
   try:
      request.session.clear()
   except:
      pass
   return redirect(index)

def index(request):
    if request.session.has_key('username'):
        return home(request,request.session['username'])
    else: 
        return render(request, 'UserViews/newindex.html')

def reportCrime(request):
    if request.method == "POST":
        location = request.POST.get('location')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        crimeType = request.POST.get('crimeType')
        crimeLevel = request.POST.get('crimeLevel')
        crimeDetails = request.POST.get('crimeDetails')
        #print("lat :",lat,"lng :",lng)
        #print('location: ',location)
        load_dotenv()
        location = {"lat": lat, "lng": lng, "location": location, "crimeType":crimeType,"crimeLevel":crimeLevel,"crimeDetails":crimeDetails}
        print(location)
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






