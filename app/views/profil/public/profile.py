from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from ....models import CustomUser
from ...decorators import login_required, request_type, RequestType
from ....http import HttpResponseNotifError, HttpResponseNotifSuccess
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

    return render(request, 'profile/profile.html', {'user': request.user, 'friends': request.user.friends.all()})


