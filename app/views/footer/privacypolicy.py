from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from ..decorators import login_required, request_type, RequestType

@login_required
@request_type(RequestType.GET)
def privacypolicy(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de politique de confidentialité

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de politique de confidentialité
    '''
    return render(request, 'footer/privacypolicy.html')
