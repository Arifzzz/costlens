from django.urls import path  # Lets me create URL routes for each page                    
from . import views  # Imports all view functions from views.py                     #The purpose of urls.py in Django is to act like the navigation map of the website. It tells Django what page to open when a user visits a specific URL.

urlpatterns = [
    path("", views.landing, name="landing"),  # Homepage / first page users see
    path("signup/", views.signup, name="signup"),  # Sign up page for new users
    path("login/", views.user_login, name="login"),  # Login page
    path("logout/", views.user_logout, name="logout"),  # Logs user out safely

    path("dashboard/", views.dashboard, name="dashboard"),  # Main user dashboard after login
    path("budget/", views.budget, name="budget"),  # Budget calculator page
    path("cost-of-living/", views.cost_of_living, name="cost_of_living"),  # Compare cities / affordability page

    path("profile/", views.profile, name="profile"),  # User account settings page
    path("history/", views.history, name="history"),  # Shows saved previous results
]