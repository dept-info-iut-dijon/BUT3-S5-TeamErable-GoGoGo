from django.urls import path

from . import views

urlpatterns = [
    path("favicon.ico", views.favicon, name="favicon"),
    path("header-pfp", views.header_pfp, name="header_pfp"),
    path("header-profile-name", views.header_profile_name, name="header_profile_name"),
    path("", views.index, name="index"),
    path("login", views.login_, name="login"),
    path("logout", views.logout_, name="logout"),
    path("register", views.register, name="register"),
    #path("settings", views.settings, name="settings"),
    path("profile", views.profile, name="profil"),
    path("change-pfp", views.change_pfp, name="change_pfp"),
    path("change-user-info", views.change_user_info, name="change_user_info"),
    path("change-pwd", views.change_pwd, name="change_pwd"),
    path("search-notfriend-user", views.search_notfriend_user, name="search_notfriend_user"),
    path("friend-list", views.friend_list, name="friend_list"),
    path("termsofuse", views.termsofuse, name="termsofuse"),
    path("privacypolicy", views.privacypolicy, name="privacypolicy"),
    path("legalmention", views.legalmention, name="legalmention"),
    path("history", views.history, name="history"),
    path("team", views.team, name="team"),
    path("help", views.help, name="help"),
    path("forgotten-password", views.forgotten_password, name="forgotten-password"),
    path("password_reset_confirm/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("add-friend", views.add_friend, name="add_friend"),
    path("delete-friend", views.delete_friend, name="delete_friend"),
    path("delete-account", views.delete_account, name="delete_account"),

    #Tournois
    path("tournament", views.tournament, name="tournament"),
    path("tournament/<id>/", views.tournament_manager, name="tournament_manager"),
    #Parties
    path("create-game", views.create_game, name="create_game"),
    path("join-game", views.join_game, name="join_game"),
    path("search-game", views.search_game, name="search_game"),
    path("game", views.game, name="game"),
    path("create-tournament", views.create_tournament, name="create_tournament"),

]
