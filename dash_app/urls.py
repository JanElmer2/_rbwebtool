from django.urls import path
from .views import DashApp
from.dash_apps import covid_dash

urlpatterns = [
    path('dash_app.html', DashApp, name='dash-app'),
]