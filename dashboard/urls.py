from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("budget/", views.budget, name="budget"),
    path("cost-of-living/", views.cost_of_living, name="cost_of_living"),

    path("profile/", views.profile, name="profile"),
    path("history/", views.history, name="history"),
]