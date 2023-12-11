from django.shortcuts import render
from ...decorators import login_required, request_type, RequestType
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ....models import CustomUser

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