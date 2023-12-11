from django.http import HttpResponse, HttpResponseRedirect
import requests
from django.views import View
from .models import Brewery, Rating
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('profile')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')

def profile(request):
    return render(request, 'profile.html')

def add_rating(request, brewery_id):
    brewery = Brewery.objects.get(pk=brewery_id)

    if request.method == 'POST':
        brewery = Brewery.objects.get(pk=brewery_id)
        stars = request.POST.get('stars')
        comment = request.POST.get('comment')
        Rating.create_rating(brewery=brewery, stars=stars, comment=comment)
        # Validate input if needed
        return redirect('brewery_detail', brewery_id=brewery_id)

    return render(request, 'add_rating.html', {'brewery': brewery})

class DeleteRatingView(View):
    def post(self, request, rating_id):
        Rating.delete_rating(rating_id)
        return redirect('all_ratings')
    
def brewery_list(request):
    api_url = 'https://api.openbrewerydb.org/v1/breweries'
    response = requests.get(api_url)
    breweries = response.json()

    context = {'breweries': breweries}
    return render(request, 'brewery_list.html', context)

def all_ratings(request):
    # Retrieve all ratings from the database
    # Pass the ratings to the template for rendering
    ratings = Rating.objects.all()
    return render(request, 'all_ratings.html', {'ratings': ratings})

def brewery_search(request):
    breweries = []
    error_message = ''
    city = ''

    if request.method == 'POST':
        city = request.POST.get('city')

        # Make API request to Open Brewery DB
        api_url = f'https://api.openbrewerydb.org/breweries?by_city={city}'
        response = requests.get(api_url)

        if response.status_code == 200:
            breweries = response.json()
        else:
            error_message = 'Error fetching breweries from the API.'

    return render(request, 'brewery_search.html', {'breweries': breweries, 'city': city, 'error_message': error_message})

def brewery_detail(request, brewery_id):
    api_url = f'https://api.openbrewerydb.org/breweries/{brewery_id}'
    response = requests.get(api_url)

    if response.status_code == 200:
        brewery = response.json()
        return render(request, 'brewery_detail.html', {'brewery': brewery})
    else:
        error_message = 'Error fetching brewery details from the API.'
        return render(request, 'brewery_search.html', {'error_message': error_message})


