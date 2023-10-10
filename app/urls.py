from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_, name="login"),
    path("register", views.register, name="register"),
    path("friends", views.friends, name="friends"),
    path("delfriends", views.delfriends, name="delfriends"),
    path("addfriends", views.addfriends, name="addfriends")
]
