from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm
from .models import Meep, Profile


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    meeps = None
    if request.user.is_authenticated:
        meeps = Meep.objects.all().order_by('-created_at')
    return render(request, 'musker/home.html', {'meeps': meeps})


def profile_list(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'musker/profile_list.html', {'profiles': profiles})
    messages.warning(request, ('You must be logged in to view this page'))
    return redirect('home')


def profile(request: HttpRequest, pk: int) -> HttpResponse:
    """
    View a Single profile
    """
    if request.user.is_authenticated:
        # Get user profile
        profile = Profile.objects.get(user_id=pk)
        # Get the user"s meeps
        meeps = Meep.objects.filter(user_id=pk).order_by('-created_at')
        # Perform form logic on follow/unfollow other user
        if request.method == 'POST':
            # Get the current logged in user's profile
            current_user_profile: Profile = request.user.profile
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
        return render(request, 'musker/profile.html', {'profile': profile, 'meeps': meeps})
    messages.warning(request, ('You must be logged in to view this page'))
    return redirect('home')


def login_user(request: HttpRequest) -> HttpResponse:
    """
    Login a user and redirect to home if authetication ok
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!!\nGet Meeping!'))
            return redirect('home')
        else:
            messages.warning(request, ('There was an error logging in. Please Try Again...'))
            return redirect('login')
    else:  # GET
        return render(request, 'login.html', {})


def logout_user(request: HttpRequest) -> HttpResponse:
    """Logout the user and redirect to home page

    Args:
        request (HttpRequest): request

    Returns:
        HttpResponse
    """
    logout(request)
    messages.success(request, ('You have been logged out. Sorry to Meep You Go'))
    return redirect('home')


def register_user(request: HttpRequest) -> HttpResponse:
    """
    Register a new user. If successfully sent it to the home page
    :param request:
    :return: Response
    """
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user=user)
            messages.success(request, ('You have successfully registered! Welcome!'))
            # Send user home
            return redirect('home')
        return render(request, 'register.html', {'form': form})
