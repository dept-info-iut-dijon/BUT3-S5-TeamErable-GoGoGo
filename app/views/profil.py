from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def profil(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'GET':
        return render(request, 'profil.html', {'user': request.user})

def change_user_info(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')

        if name:
            request.user.username = name
        if email:
            request.user.email = email
        
        request.user.save()
        return HttpResponse('<p class="success">Les informations ont bien été modifiées.</p>')
    
    return HttpResponse('<p class="error">Une erreur est survenue.</p>')

def change_pfp(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'POST':
        pfp = request.FILES.get('pfp')
        if pfp:
            request.user.profile_picture = pfp
            request.user.save()
            return HttpResponse('<p class="success">La photo de profil a bien été modifiée.</p>')
    
    return HttpResponse('<p class="error">Une erreur est survenue.</p>')

def change_user_info(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')

        if name:
            request.user.username = name
        if email:
            request.user.email = email
        
        request.user.save()
        return HttpResponse('<p class="success">Les informations ont bien été modifiées.</p>')
    
    return HttpResponse('<p class="error">Une erreur est survenue.</p>')

def change_pfp(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'POST':
        pfp = request.FILES.get('pfp')
        if pfp:
            request.user.profile_picture = pfp
            request.user.save()
            return HttpResponse('<p class="success">La photo de profil a bien été modifiée.</p>')
    
    return HttpResponse('<p class="error">Une erreur est survenue.</p>')