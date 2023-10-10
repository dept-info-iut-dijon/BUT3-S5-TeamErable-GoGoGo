from django.urls import path

from . import views

urlpatterns = [
    path("header-pfp", views.header_pfp, name="header_pfp"),
    path("header-profile-name", views.header_profile_name, name="header_profile_name"),
    path("", views.index, name="index"),
    path("login", views.login_, name="login"),
    path("logout", views.logout_, name="logout"),
    path("register", views.register, name="register"),
    path("friends", views.friends, name="friends"),
    path("settings", views.settings, name="settings"),
    path("delfriends", views.delfriends, name="delfriends"),
    path("addfriends", views.addfriends, name="addfriends")
]
