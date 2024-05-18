
from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse 
from django.core.files.storage import FileSystemStorage
import urllib.parse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json
import pymongo
from datetime import datetime

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://samitsinghvi:sam16%40MONGO@cluster0.v5kwwe5.mongodb.net/"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['HealthTracker']
coll = db['nutrientData']




#Aas8QN2mLYFLeo11M9pV4Q==ojNlGuRVdNmbaAMX
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:     
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                print("##################")
                print(form.cleaned_data)
                messages.success(request, "Account created successfully for " + username)
                add_user_to_mongo(username, form.cleaned_data.get('height'), form.cleaned_data.get('weight'))
                return redirect('home')
        context = {'form': form}
        return render(request, 'register.html', context)

def add_user_to_mongo(username, height, weight):
    coll.insert_one({
        'username': username,
        'height': height,
        'weight': weight,
        'proteins' : 0,
        'sugar' : 0,
        'carbs': 0,
        'calories': 0,
        'fat': 0,
        'date': ""
    })

def user_login(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password) 
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                messages.info(request, "USERNAME or password is wrong")
        context = {}
        return render(request, 'login.html', context)  


def user_logout(request):
        logout(request)
        return redirect('login')

@login_required(login_url='login')
def home(request):
    import requests
    import json
    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query , headers = {'X-Api-Key':'Aas8QN2mLYFLeo11M9pV4Q==ojNlGuRVdNmbaAMX'})
        try:
            api = json.loads(api_request.content)
            username = request.user.username

            filter = {'username' : username}
            target = coll.find_one({'username' : username})
            date = datetime.now().date()    

            newvalues = { "$set": { 'carbs': float(target['carbs']) +  float(api[0]['carbohydrates_total_g']),
                                   'calories' : float(target['calories']) +  float(api[0]['calories']),
                                   'fat' : float(target['fat']) +  float(api[0]['fat_total_g']),
                                   'date' : str(date),
                                   'proteins' : float(target['proteins']) +  float(api[0]['protein_g']),
                                   'sugar' : float(target['sugar']) +  float(api[0]['sugar_g']),

                                   } }

            coll.update_one(filter,newvalues)
            if target['calories']>2200:
                messages.info(request, "You are crossing calories limit of your day : " + str(target['calories']))

            if target['fat']>75:
                messages.info(request, "You are crossing fat limit of your day : " + str(target['calories']))
            
            if target['carbs']>365:
                messages.info(request, "You are crossing carbs limit of your day : " + str(target['carbs']))
            # coll.insert_one(records)

            

            print(api_request.content)
            print(username)
        except Exception as e:
            api = "oops! There was an error"
            print(e)
        return render(request, 'home.html',{'api':api})
    else:
         return render(request, 'home.html',{'query':'Enter a valid query'})


    return render(request , 'home.html')


    
@login_required(login_url='login')
def streamlit_app(request):
    # Redirect to the Streamlit app URL
    return redirect('http://localhost:8501')
    

@login_required(login_url='login')
def update_search_bar(request):
    if request.method == 'POST':
        prediction_result = request.POST.get('prediction', '')
        # Update your search bar with the prediction result
        # Example: You can pass the prediction result to the template context
        return render(request, 'home.html', {'prediction_result': prediction_result})
    else:
        return HttpResponse("Method not allowed", status=405)


def profile(request):
    username = request.user.username
    
    context = {
        'username': username,
        'target' : coll.find_one({'username' : username})
    }
    
    

    return render(request, 'profile.html', context)