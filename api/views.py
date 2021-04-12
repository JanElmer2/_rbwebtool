from django.shortcuts import render


def BloombergAPI(request):
    return render(request, 'api/bloomberg_api.html', {})