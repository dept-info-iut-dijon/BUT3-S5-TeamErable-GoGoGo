from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def tournoisid(request: HttpRequest, id:int) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    
    return render(request, 'tournois/tournoisgestion.html')