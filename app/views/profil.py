from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..forms.Profil import Profil

def profil(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: 
        return HttpResponseRedirect('/login')

    if request.method == 'GET':
        return render(request, 'profil.html', {'user': request.user})

    if request.method == 'POST':
        form = Profil(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            print(request.FILES)
            if 'profile_picture' in request.FILES:
                request.user.profile_picture.save(request.FILES['profile_picture'].name, request.FILES['profile_picture'])
            form.save()
            
    else:
        form = Profil(instance=request.user)

    return render(request, 'profil.html', {'form': form})