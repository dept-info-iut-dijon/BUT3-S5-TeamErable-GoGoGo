from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from ..decorators import login_required, request_type, RequestType

@login_required
@request_type(RequestType.GET)
def team(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page d'équipe

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête d'équipe
    '''
    return render(request, 'team.html')
