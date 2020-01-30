from django.shortcuts import render,redirect
import pymongo
import os
from dotenv import load_dotenv
from bson.json_util import dumps
from django.http import JsonResponse
from django.http import HttpResponse
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
import requests
import json
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

from . import RT




# from twilio.rest import Client


# Create your views here.
client = pymongo.MongoClient("mongodb+srv://"+str(os.getenv("USER"))+":"+str(os.getenv("PASSWORD"))+"@devcluster-qbbgy.mongodb.net/Sahyog?retryWrites=true&w=majority")
db = client.Sahyog
locationDB = db.Location
validateDB = db.Validate

def admindashboard(request):
    if request.method == "POST":
        print("POST HITTED")
        location = request.POST.get('Location')
        # print(location)
        validations=(list(validateDB.find({'location':location})))
        print("validations are",validations)
        return render(request,'adminarea/validators.html', {"validations":validations})
        # return HttpResponse("Hello")
    else:
        return render(request,'adminarea/index.html')

def validators(request):
    if request.method=="POST":
        # print(request.POST.get('hid'))
        obj=locationDB.find_one({"_id":ObjectId(request.POST.get('hid'))})
        return render(request,'adminarea/validators.html',{"ctype":obj['crimeType'],"location":obj['location'],"clevel":obj['crimeLevel'],"cdet":obj['crimeDetails'],"name":obj['userName'],"email":obj['email'],"stat":obj['status'],"phone":obj['phone']})
    else:
        redirect(admindashboard)


def status(request):
    locatn=[]
    ctype=[]
    clevel=[]
    uName=[]
    email=[]
    stat=[]
    ph=[]
    cdet=[]


    locations = json.loads(dumps(locationDB.find()))
    # print(locations)
    for i in range(len(locations)):
        item=locations[i]
        locatn.append(item["location"])
        ctype.append(item['crimeType'])
        clevel.append(item['crimeLevel'])
        cdet.append(item['crimeDetails'])
        email.append(item['email'])
        ph.append(item['phone'])
        stat.append(item['status'])
        uName.append(item['userName']) 
    mylist1 = mylist2 = mylist = zip(locatn, ctype, clevel, cdet, email, ph, stat, uName) 
    print(locatn)
    return render(request,'adminarea/status.html',context ={"reports":mylist,"reports2":mylist2,"reports1":mylist1})
    
# def validators(request):
#     if request.method == "POST":
#         print("POST HITTED")
#         location = request.POST.get('Location')
#         # print(location)
#         validations=(list(validateDB.find({'location':location})))
#         print("validations are",validations)
#         # if len(validations) == 0 :
#         #     return render(request,'adminarea/validators.html', {"validations":"nothing"})
        
            
#         return render(request,'adminarea/validators.html', {"validations":validations})

def predictCrime(request):
    preds = RT.predict(308,0.00124153,992,53.1,0.1154,0.00125,0.6651088,107,0.000001417,50.47,90366,9.2)
    return render(request,'adminarea/predictCrime.html', {"murder":preds[0],"rape":preds[1],"robbery":preds[2],"kidnapping":preds[3],"riots":preds[4]})

    





    
    
    


    
         
    


        
    

# def makeCall(request):
    
#     # Your Account Sid and Auth Token from twilio.com/console
#     # DANGER! This is insecure. See http://twil.io/secure
#     account_sid = 'ACc4b67eb6c1d521f75d927122e60e1719'
#     auth_token = 'b541bf5e349b93c95d0e1556bc77b2ba'
#     client = Client(account_sid, auth_token)

#     call = client.calls.create(
#                             url='http://demo.twilio.com/docs/voice.xml',
#                             to=,
#                             from_='+15017122661'
#                         )

#     print(call.sid)
#     return 

