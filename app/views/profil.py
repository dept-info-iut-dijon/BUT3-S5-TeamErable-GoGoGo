from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def profil(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: 
        return HttpResponseRedirect('/login')

    if request.method == 'GET':
        return render(request, 'profil.html', {'user': request.user})
