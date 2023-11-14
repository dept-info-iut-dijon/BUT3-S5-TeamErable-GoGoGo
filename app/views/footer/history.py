from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from ..decorators import login_required, request_type, RequestType

@login_required
@request_type(RequestType.GET)
def history(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page d'histoire

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête d'histoire
    '''
    return render(request, 'footer/history.html')
