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
validateDB = db.Validate

class RegisterForm(forms.ModelForm):
    phone_number = forms.CharField(required=True, max_length=13,widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control"}))
    name = forms.CharField(required=True, max_length=13,widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required=True, max_length=30,widget=forms.TextInput(attrs={'class': "form-control"}))
    emergency_contact_1 = forms.CharField(required=True, max_length=13,widget=forms.TextInput(attrs={'class': "form-control"}))
    emergency_contact_2 = forms.CharField(required=True, max_length=13,widget=forms.TextInput(attrs={'class': "form-control"}))
    class Meta:
        model = User
        fields = (
            'phone_number',
            'password1',
            'name',
            'email',
            'emergency_contact_1',
            'emergency_contact_2',
            
        )

class LoginForm(forms.ModelForm):
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control"}))
    class Meta:
        model = User
        fields = ('phone', 'password')

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

def index(request,username=None):
    if request.session.has_key('username'):
         return render(request, 'UserViews/newindex.html',{"username":request.session["name"]})
    else: 
        return render(request, 'UserViews/newindex.html',{"username":None})


def safey(request):
    if request.session.has_key('username'):
        return render(request, 'UserViews/safey.html',{"username":request.session["name"]})
    else:
        return render(request, 'UserViews/safey.html',{"username":None})

def report(request):
    if request.session.has_key('username'):
        return render(request, 'UserViews/report.html',{"username":request.session["name"]})
    else:
        return redirect(index,None)



# @describe: Register new user 
def register(request):
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = {
                # "username": form.cleaned_data["username"], 
                # "fname": form.cleaned_data["first_name"],
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password1"],
                "phone": '+91'+ form.cleaned_data["phone_number"],
                # "home": form.cleaned_data["home_address"],
                # "work": form.cleaned_data["work_address"],
                "ec1": '+91'+ form.cleaned_data["emergency_contact_1"],
                "ec2": '+91'+ form.cleaned_data["emergency_contact_2"]
            }
            return redirect(validateOTP, json.dumps(user))
    else:
        if request.session.has_key('username'):
            return index(request,request.session['name'])
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
            request.session['username'] = userObj["phone"]
            request.session['name'] = userObj["name"]
            request.session['email'] = userObj["email"]
            request.session['ec1'] = userObj["ec1"]
            request.session['ec2'] = userObj["ec2"]
            return redirect(index, request.session["name"])

    request.session["otp"] = OTPGenerator()
    msg = 'Your OTP is '+request.session['otp']
    sendSMS(userObj['phone'],msg)    
    return render(request, 'UserViews/OTP.html')
     
# @describe: Existing user login
def login(request):
    if request.session.has_key('username'):
        return redirect(index, {"username": request.session['name']})
    else:
        if request.method=="POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                # try:
                    username = form.cleaned_data["phone"]
                    print("phone ",username)
                    username="+91"+username
                    user = userDB.find_one({"phone": username})
                    print("userpass: "+user["password"]+" formpass: "+form.cleaned_data["password"])
                    if user["password"] == form.cleaned_data["password"]:
                        request.session["username"] = username
                        request.session['name'] = user["name"]
                        request.session['email'] = user["email"]
                        request.session["ec1"] = user["ec1"]
                        request.session["ec2"] = user["ec2"]
                        print("validdd")
                        return redirect(index,request.session['name'])
                # except:
                #     return redirect(register)
            else:
                print("form not valid")
                return render(request, 'UserViews/login.html', {"form": form})
        else:
            form = LoginForm()
        print("reached")
        return render(request, 'UserViews/login.html', {"form": form})

# def home(request, username):
#     if request.session.has_key('username'):
#         return render(request, 'UserViews/home.html', {"username": username})
#     else: 
#         return redirect(index)

def logout(request):
   try:
      request.session.clear()
   except:
      pass
   return redirect(index)



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
        location = {"lat": lat, "lng": lng, "location": location, "crimeType":crimeType,"crimeLevel":crimeLevel,"crimeDetails":crimeDetails,"count":0}
        print(location)
        locationDB.insert_one(location)        
        return HttpResponse(json.dumps({'status':'success','latitude':lat,'longitude':lng}),content_type='application/json')
        
    else:
        return render(request,'UserViews/report.html')

# Analyse statistics dashboard...
def analytics(request):
    locations = list(locationDB.find({"severity": "2"}))
    if request.session.has_key('username'):
        return render(request, 'UserViews/analytics.html', {"total_crimes": len(locations), "username": request.session['name']})
    else:
        return render(request, 'UserViews/analytics.html', {"total_crimes": len(locations)})
    

# A function for server sent events.... 
# @describe: Add new markers dynamically on to map, without refreshing page...
def SSE(request):
    locations = dumps(locationDB.find())
    # validators = dumps(validateDB.find())
    return HttpResponse(
        "data: "+locations+"\n\n",
        
        content_type='text/event-stream'
    )

def validate(request):
    if request.session.has_key('username'):
        return render(request, 'UserViews/validate.html',{"username":request.session["name"]})
    else:
        return redirect(index,None)



def validateCrime(request):
    if request.method == "POST":
        username = request.session['username']
        location = request.POST.get('Location')
        check = validateDB.find_one({'username' :username,"location":location})
        if check == None:
            data = userDB.find({'username' :username})
            count = 0

            for items in data:
                name = items['name']
                # lname = items['lname']
                email = items['email']
                # phone = items['phone']

                # count = items['count']
            # print(fname,lname,email,phone)
            temp = (locationDB.find({"location":location}))
            count = 0
            id = 0
            lat = 0
            lng = 0
            location = 0
            crimeType = 0
            crimeDetails = 0
            meranaam = ""


            for temps in temp:
                ids = temps['_id']
                lat = temps['lat']
                lng = temps['lng']
                location = temps['location']
                meranaam = location
                crimeDetails = temps['crimeDetails']
                crimeType = temps['crimeType']
                count = temps['count']

            count = count +1
            printer_c_name = {
                'location' : meranaam
            }
            printer_c_price_update={
                '$set' : {
                    'count': count
                }
            }
            locationDB.update_one(printer_c_name,printer_c_price_update)
            
            # temp.update_one({'_id':ids,
            #                 'lat':lat,
            #                 'lng':lng,
            #                 'location':location,
            #                 'crimeType':crimeType,
            #                 'crimeDetails':crimeDetails,
            #                 'count':count}) 

            
            # for count in counts:
            #     count = count +1

            # validation = {"username" : username,"location":location}

            validation = {"username" : username,"name":name,"email":email,"location":location}
 
            validateDB.insert_one(validation)
            return HttpResponse(json.dumps({'status':'You have successfully validated this crime.'}),content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'You have already validated this crime.'}),content_type='application/json')

        
    else:
        return redirect(validate)








