from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import MeepForm, ProfilePicForm, SignUpForm
from .models import Meep, Profile


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    meeps = None
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            meep = form.save(commit=False)
            meep.user = request.user
            meep.save()
            messages.success(request, ("Your Meep Has Been Posted!"))
            return redirect("home")
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, "musker/home.html", {"meeps": meeps, "form": form})
    else:
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, "musker/home.html", {"meeps": meeps})


def profile_list(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "musker/profile_list.html", {"profiles": profiles})
    messages.warning(request, ("You must be logged in to view this page"))
    return redirect("home")


def unfollow(request: HttpRequest, pk: int) -> HttpResponse:
    """unfollow Unfollow a user

    Arguments:
        request -- Current Request
        pk -- User primary key

    Returns:
        Response
    """
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile: Profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.follows.remove(profile)
        # Save the removed profile
        request.user.profile.save()

        # Return message
        messages.success(
            request=request,
            message=f"You have successfully unfollowed {profile.user.username} ({profile.user.first_name} {profile.user.last_name})",
        )
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.warning(request, ("You must be logged in to view this page"))
        return redirect("home")


def follow(request: HttpRequest, pk: int) -> HttpResponse:
    """unfollow Follow a user

    Arguments:
        request -- Current Request
        pk -- User primary key

    Returns:
        Response
    """
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(pk=pk)
        # Follow the user
        request.user.profile.follows.add(profile)
        # Save the removed profile
        request.user.profile.save()

        # Return message
        messages.success(
            request=request,
            message=f"You have successfully followed {profile.user.username} ({profile.user.first_name} {profile.user.last_name})",
        )
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.warning(request, ("You must be logged in to view this page"))
        return redirect("home")


def profile(request: HttpRequest, pk: int) -> HttpResponse:
    """
    View a Single profile
    """
    if request.user.is_authenticated:
        # Get user profile
        profile = Profile.objects.get(user_id=pk)
        # Get the user"s meeps
        meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")
        # Perform form logic on follow/unfollow other user
        if request.method == "POST":
            # Get the current logged in user's profile
            current_user_profile: Profile = request.user.profile
            # Get form data
            action = request.POST.get("follow")
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save()

        # Render the profile view
        return render(
            request, "musker/profile.html", {"profile": profile, "meeps": meeps}
        )
    messages.warning(request, ("You must be logged in to view this page"))
    return redirect("home")


def login_user(request: HttpRequest) -> HttpResponse:
    """
    Login a user and redirect to home if authetication ok
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!!\nGet Meeping!"))
            return redirect("home")
        else:
            messages.warning(
                request, ("There was an error logging in. Please Try Again...")
            )
            return redirect("login")
    else:  # GET
        return render(request, "login.html", {})


def logout_user(request: HttpRequest) -> HttpResponse:
    """Logout the user and redirect to home page

    Args:
        request (HttpRequest): request

    Returns:
        HttpResponse
    """
    logout(request)
    messages.success(request, ("You have been logged out. Sorry to Meep You Go"))
    return redirect("home")


def register_user(request: HttpRequest) -> HttpResponse:
    """
    Register a new user. If successfully sent it to the home page
    :param request:
    :return: Response
    """
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]

            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user=user)
            messages.success(request, ("You have successfully registered! Welcome!"))
            # Send user home
            return redirect("home")
    return render(request, "register.html", {"form": form})


def update_user(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        user_id: int = request.user.id
        current_user = User.objects.get(pk=user_id)
        profile_user = Profile.objects.get(user_id=user_id)

        # Get forms
        # Insert current user info into the signup form
        user_form = SignUpForm(
            request.POST or None, request.FILES or None, instance=current_user
        )
        profile_form = ProfilePicForm(
            request.POST or None, request.FILES or None, instance=profile_user
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, user=current_user)
            messages.success(request, ("Your Profile has been updated!"))
            return redirect("home")

        return render(
            request,
            "update_user.html",
            {"user_form": user_form, "profile_form": profile_form},
        )
    else:
        messages.warning(request, ("You must be logged in to view that page..."))
        return redirect("home")


def meep_like(request: HttpRequest, pk: int) -> HttpResponse:
    """meep_like Which meep a User likes

    Arguments:
        request: HTTPRequest -- The request object
        pk: int -- The primary key

    Returns:
        the response
    """

    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)

        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.warning(request, ("You must be logged in to view that page..."))
        return redirect("home")


def meep_share(request: HttpRequest, pk: int) -> HttpResponse:
    """meep_share Share a Meep

    Arguments:
        request -- The request
        pk -- The prmary key of the meep to share

    Returns:
        A response with a template
    """
    meep = get_object_or_404(Meep, pk=pk)

    if meep:
        return render(
            request, template_name="musker/show_me.html", context={"meep": meep}
        )
    else:
        messages.error(request=request, message="That Meep does not exist.")
        return redirect("home")
