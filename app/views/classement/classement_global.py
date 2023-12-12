from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from ..decorators import login_required, request_type, RequestType

@login_required
@request_type(RequestType.GET)
def classement_global(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de classement global

    Args:
        request (HttpRequest): Requete HTTP

    Returns:
        HttpResponse: Reponse HTTP de la page de classement global
    '''

    return render(request, 'classement/global.html', {'user': request.user, 'friends': request.user.friends.all()})