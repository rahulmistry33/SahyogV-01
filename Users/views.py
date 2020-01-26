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
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


client = pymongo.MongoClient("mongodb+srv://"+str(os.getenv("USER"))+":"+str(os.getenv("PASSWORD"))+"@devcluster-qbbgy.mongodb.net/Sahyog?retryWrites=true&w=majority")
db = client.Sahyog
users = db.Location

# Create your views here.

def SOS(request):
    to = '+9184520 70570'
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    response = client.messages.create(
    body='Get me a pizza, with extra cheese, and also a burger, and some choco chipss :)', 
    to=to, from_=os.getenv('TWILIO_PHONE_NUMBER'))
    return HttpResponse("hello")


def index(request):
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
    # print(locations)
    return HttpResponse(
        "data: "+locations+"\n\n",
        content_type='text/event-stream'
    )


def register(request):
    form = UserCreationForm()
    return render(request, 'UserViews/register.html', {"form": form})





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





