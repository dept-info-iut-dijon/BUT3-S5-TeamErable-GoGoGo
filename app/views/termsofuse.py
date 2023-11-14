from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .decorators import login_required, request_type, RequestType

@login_required
@request_type(RequestType.GET)
def termsofuse(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de conditions d'utilisation

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de conditions d'utilisation
    '''
    return render(request, 'termsofuse.html')
