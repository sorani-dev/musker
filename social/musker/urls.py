from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path("profile/<int:pk>", views.profile, name='profile'),
    path("profile/followers/<int:pk>", views.followers, name='profile_followers'),
    path("profile/follows/<int:pk>", views.follows, name='profile_follows'),
    
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path("update_user/", views.update_user, name="update_user"),
    
    path("meep_like/<int:pk>", views.meep_like, name="meep_like"),
    path("meep_share/<int:pk>", views.meep_share, name="meep_share"),
    path("delete_meep/<int:pk>", views.meep_delete, name="meep_delete"),
    path("edit_meep/<int:pk>", views.meep_edit, name="meep_edit"),
            
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
    
    path('search/', views.search, name='search'),
    path('search_user/', views.search_user, name='search_user'),
]
