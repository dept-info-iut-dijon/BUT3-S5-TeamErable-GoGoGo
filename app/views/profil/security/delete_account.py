from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from ....models import CustomUser
from ...decorators import login_required, request_type, RequestType
from ....http import HttpResponseNotifError, HttpResponseNotifSuccess
import os

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