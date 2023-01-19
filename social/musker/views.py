from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import Profile


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'musker/home.html', {})


def profile_list(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'musker/profile_list.html', {'profiles': profiles})
    messages.warning(request, ('You must be logged in to view this page'))
    return redirect('home')

def profile(request: HttpRequest, pk:int)->HttpResponse:
    """
    View a Single profile
    """
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        return render(request, 'musker/profile.html', {'profile': profile})
    messages.warning(request, ('You must be logged in to view this page'))
    return redirect('home')
