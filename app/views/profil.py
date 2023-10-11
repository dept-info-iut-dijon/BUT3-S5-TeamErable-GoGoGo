from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..forms.Profil import Profil

def profil(request: HttpRequest) -> HttpResponse:
    donnees = {
        'username': "ffff",
        'email' : "sdfnsifo@sfissdi.sfsijf",
        'password1' : "sfdsf",
        'password2' : "ondfsdnf",
    }

    form = Profil(request.POST, initial=donnees)

    if not request.user.is_authenticated: 
        return HttpResponseRedirect('/login')

    #if request.method == 'GET':
    
    
    print(form)
    return render(request, 'profil.html', {'form':form})
