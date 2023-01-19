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
        # Get user profile
        profile = Profile.objects.get(user_id=pk)
        # Perform form logic on follow/unfollow other user
        if request.method == 'POST':
            # Get the current logged in user's profile
            current_user_profile:Profile = request.user.profile
            # Get form data
            action = request.POST.get('follow')
            # Decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save()
        
        # Render the profile view
        return render(request, 'musker/profile.html', {'profile': profile})
    messages.warning(request, ('You must be logged in to view this page'))
    return redirect('home')
