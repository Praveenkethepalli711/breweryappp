from . import views
from django.urls import path
from .views import DeleteRatingView




urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.LoginPage,name='login'),
    path('signup/', views.SignupPage,name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.LogoutPage,name='logout'),
    path('brewery_list/', views.brewery_list, name='brewery_list'),  # Add this line for the root path
    path('brewery_search/', views.brewery_search, name='brewery_search'),
    path('brewery_detail/<uuid:brewery_id>/', views.brewery_detail, name='brewery_detail'),
    path('add_rating/<uuid:brewery_id>/', views.add_rating, name='add_rating'),
    path('delete_rating/<int:rating_id>/', DeleteRatingView.as_view(), name='delete_rating'),
    path('all_ratings/', views.all_ratings, name='all_ratings')
]