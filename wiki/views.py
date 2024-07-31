from django.shortcuts import render

# Create your views here.

def wiki(request):
    return render(request, 'wiki.html')