from django.shortcuts import render

def DashApp(request):
    return render(request, 'dash_app/dash_app.html', {})