from django.shortcuts import render
from django.http import HttpResponse

def event_list(request):
    """Event list view"""
    return HttpResponse("Events list - Coming soon!")
