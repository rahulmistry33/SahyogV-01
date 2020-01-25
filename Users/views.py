from django.shortcuts import render
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

client = pymongo.MongoClient("mongodb+srv://"+str(os.getenv("USER"))+":"+str(os.getenv("PASSWORD"))+"@devcluster-qbbgy.mongodb.net/Sahyog?retryWrites=true&w=majority")
db = client.Sahyog
users = db.Location




# Create your views here.

def home(request):
    return render(request, 'UserViews/home.html')

def safey(request):
    return render(request, 'UserViews/safey.html')

def report(request):
    return render(request, 'UserViews/report.html')

def SOS(request):    
    
    myphnos =['+919987718876','+918879272265']    
    
    for i in myphnos:
        to = i
        client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        response = client.messages.create(
        body='This is to inform you that your ward/friend is in danger and awaits your help. Access their location using the following link '+'http://www.google.com/maps/place/19.0729578,72.8999708', 
        to=to, from_=os.getenv('TWILIO_PHONE_NUMBER'))

    return render(request, 'UserViews/SOS.html')




def index(request):
    if request.method == "POST":
        location = request.POST.get('location')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        #print("lat :",lat,"lng :",lng)
        #print('location: ',location)
        load_dotenv()        
        location = {"lat": lat, "lng": lng, "location": location }
        users.insert_one(location)        
        return HttpResponse(json.dumps({'status':'success','latitude':lat,'longitude':lng}),content_type='application/json')
        
    else:
        return render(request,'UserViews/user.html')

        """print(r['Response']['View'][3]['Location']['DisplayPosition']['Lattitude'])"""
        """context = {
            'lat':latitude,
            'long':longitude
        }"""
        """return render(request,'UserViews/user.html',context)"""


def random(request):
    locations = dumps(users.find())
    #print(locations)
    return HttpResponse(
        "data: "+locations+"\n\n",
        content_type='text/event-stream'
    )








        
        
       

    
  





