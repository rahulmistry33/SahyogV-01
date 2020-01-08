from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from django.http import HttpResponse






# Create your views here.

    

def index(request):
    if request.method == "POST":

        description = request.POST.get('description')
        location = request.POST.get('location')
        print("location :",location)

        #URL = "https://geocoder.ls.hereapi.com/6.2/geocode.json?apiKey=jVB385WpgHu9PmsnaQeW2-qVfltkDlccMdda8oicJQs&searchtext={}".format(location)
        url = "https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json?access_token=pk.eyJ1IjoicmFodWxtaXN0cnkzMyIsImEiOiJjazRvMmg0dGIwMjU5M2pwMWtlYmRsNmZjIn0.-b0ywtsKoCRSfL5Xd_2c0g".format(location)

        #querystring = {"callback":"test","q":"{}".format(location)}
        response = requests.get(url)
        print(response.json())
        data = response.json()
        lati = data["features"][0]["geometry"]["coordinates"][1]
        longi = data["features"][0]["geometry"]["coordinates"][0]
        # # data = response.json()
        # headers = {
        # 'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        # 'x-rapidapi-key': "fc9c30f8a3msh9def95e13319b5dp1d4d97jsnfb94187f29c2"
        # }

        # response = requests.get(url, headers=headers, params=querystring)

        # print(response.text)

        # print(data)
        # print("response isssss:",data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude'])
        # latitude = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude']
        # longitude = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']
        
        return HttpResponse(json.dumps({'status':'success','latitude':lati,'longitude':longi}),content_type='application/json')
        
    
    else:
        return render(request,'UserViews/user.html')

        
        
       

    
        
        """print(r['Response']['View'][3]['Location']['DisplayPosition']['Lattitude'])"""
        """context = {
            'lat':latitude,
            'long':longitude
        }"""
        """return render(request,'UserViews/user.html',context)"""









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






