from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from django.http import HttpResponse
import datetime

import pymongo
import dns
import os
from dotenv import load_dotenv

# Create your views here.

def index(request):
    if request.method == "POST":
        location = request.POST.get('location')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        print("lat :",lat,"lng :",lng)
        print('location: ',location)
        load_dotenv()
        client = pymongo.MongoClient("mongodb+srv://"+str(os.getenv("USER"))+":"+str(os.getenv("PASSWORD"))+"@devcluster-qbbgy.mongodb.net/Sahyog?retryWrites=true&w=majority")
        db = client.Sahyog
        users = db.Location
        location = {"lat": lat, "lng": lng, "location": location}
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
    return HttpResponse(
        'data: The server time is: %s\n\n' % datetime.datetime.now(),
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





