from django.urls import path
from .views import BloombergAPI

urlpatterns = [
    path('bloomberg_api.html', BloombergAPI, name='bloomberg_api')
]
