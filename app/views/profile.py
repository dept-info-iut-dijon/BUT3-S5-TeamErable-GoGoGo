from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from ..models import CustomUser
from .decorators import login_required, request_type, RequestType
from ..http import HttpResponseNotifError, HttpResponseNotifSuccess
import os

@login_required
@request_type(RequestType.GET)
def profile(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de profil

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la page de profil
    '''

    return render(request, 'profile.html', {'user': request.user, 'friends': request.user.friends.all()})


@login_required
@request_type(RequestType.POST)
def change_user_info(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la modification des informations de l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la modification des informations de l'utilisateur
    '''

    name = request.POST.get('username')
    email = request.POST.get('email')

    if name: request.user.username = name
    if email: request.user.email = email

    request.user.save()
    return HttpResponseNotifSuccess('Les informations ont bien été modifiées.')


def remove_pfp(path: str | None) -> None:
    '''Supprime la photo de profil d'un utilisateur

    Args:
        path (str): Chemin de la photo de profil
    '''
    if path:
        try: os.remove(path)
        except: pass


@login_required
@request_type(RequestType.POST)
def change_pfp(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la modification de la photo de profil de l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la modification de la photo de profil de l'utilisateur
    '''
    ret: HttpResponse = HttpResponseNotifError('Une erreur est survenue.')

    pfp = request.FILES.get('pfp')
    if pfp:
        if pfp.size > 2097152: # 2 * 1024 * 1024 = 2097152 (2MB)
            return HttpResponseNotifError('La photo de profil ne doit pas dépasser 2 Mo.')

        else:
            remove_pfp(request.user.profile_picture.path if request.user.profile_picture else None)

            request.user.profile_picture = pfp
            request.user.save()

            ret = HttpResponseNotifSuccess('La photo de profil a bien été modifiée.')

    return ret


@login_required
@request_type(RequestType.POST)
def change_pwd(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la modification du mot de passe de l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la modification du mot de passe de l'utilisateur
    '''
    ret: HttpResponse = HttpResponseNotifError('Une erreur est survenue.')

    old_pwd = request.POST.get('old-pwd')
    new_pwd = request.POST.get('new-pwd')
    confirm_new_pwd = request.POST.get('new-pwd-confirm')

    if old_pwd and new_pwd and confirm_new_pwd:
        if new_pwd == confirm_new_pwd:
            try:
                validate_password(new_pwd)

                if request.user.check_password(old_pwd):
                    request.user.set_password(new_pwd)
                    request.user.save()
                    request.user = authenticate(username=request.user.username, password=new_pwd)
                    if request.user: login(request, request.user)
                    ret = HttpResponseNotifSuccess('Le mot de passe a bien été modifié. Rechargement de la page...')

                else:
                    ret = HttpResponseNotifError('L\'ancien mot de passe est incorrect.')

            except Exception as e:
                ret = HttpResponseNotifError('Le mot de passe n\'est pas assez sécurisé.')

        else: ret = HttpResponseNotifError('Les mots de passe ne correspondent pas.')

    return ret


@login_required
@request_type(RequestType.GET, RequestType.POST)
def friends(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la liste d'amis de l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la liste d'amis de l'utilisateur
    '''
    listfriends = request.user.friends.all()
    return render(request, 'friends.html', {'friends': listfriends})


@login_required
@request_type(RequestType.POST)
def search_notfriend_user(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la recherche d'utilisateurs non amis de l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la recherche d'utilisateurs non amis de l'utilisateur
    '''
    ret: HttpResponse = HttpResponseBadRequest()

    query = request.POST.get('username')
    if query:
        users = CustomUser.objects.filter(username__icontains = query).exclude(id = request.user.id).exclude(friends = request.user).order_by('username')[:6]
        ret = render(request, 'reusable/search_user.html', {'users': users})

    else: ret = render(request, 'reusable/search_user.html', {'users': []})

    return ret


@login_required
@request_type(RequestType.GET, RequestType.POST)
def friend_list(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la liste d'amis de l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la liste d'amis de l'utilisateur
    '''
    ret: HttpResponse = HttpResponseBadRequest()

    if request.method == 'GET':
        listfriends = request.user.friends.all()
        ret = render(request, 'reusable/friend_list.html', {'friends': listfriends})

    return ret


@login_required
@request_type(RequestType.GET)
def add_friend(request: HttpRequest) -> HttpResponse:
    '''Controlleur de l'ajout d'un ami à l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de l'ajout d'un ami à l'utilisateur
    '''
    ret: HttpResponse = HttpResponseNotifError('Une erreur est survenue.')

    friend_id = request.GET.get('id')

    if friend_id is not None:
        friend = CustomUser.objects.get(id = friend_id)
        if not request.user.friends.filter(id = friend_id).exists() and friend:
            request.user.friends.add(friend)
            ret = HttpResponseNotifSuccess(f'{friend.username} a été ajouté à vos amis.')

    return ret


@login_required
@request_type(RequestType.GET)
def delete_friend(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la suppression d'un ami à l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la suppression d'un ami à l'utilisateur
    '''
    ret: HttpResponse = HttpResponseNotifError('Une erreur est survenue.')

    friend_id = request.GET.get('id')

    if friend_id is not None:
        friend = CustomUser.objects.get(id = friend_id)

        if request.user.friends.filter(id = friend_id).exists() and friend:
            request.user.friends.remove(friend)
            ret = HttpResponseNotifSuccess(f'{friend.username} a été supprimé de vos amis.')

    return ret


@login_required
@request_type(RequestType.POST)
def delete_account(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la suppression du compte de l'utilisateur

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de la suppression du compte de l'utilisateur
    '''
    ret: HttpResponse = HttpResponseNotifError('Une erreur est survenue.')

    password = request.POST.get('password')
    if password:
        if request.user.check_password(password):
            request.user.delete()
            ret = HttpResponseNotifSuccess('Votre compte a bien été supprimé. Redirection vers la page de connexion...')

        else: ret = HttpResponseNotifError('Le mot de passe est incorrect.')

    return ret
