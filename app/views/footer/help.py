from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from ..decorators import login_required, request_type, RequestType

@login_required
@request_type(RequestType.GET)
def help(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page d'aide

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête d'aide
    '''
    return render(request, 'footer/help.html')
