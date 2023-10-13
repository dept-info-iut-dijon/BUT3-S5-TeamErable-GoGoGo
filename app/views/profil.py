from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from ..models import CustomUser

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
            if pfp.size > 2 * 1024 * 1024:
                return HttpResponseBadRequest('<p class="error">La photo de profil est trop volumineuse.</p>')

            request.user.profile_picture = pfp
            request.user.save()
            return HttpResponse('<p class="success">La photo de profil a bien été modifiée.</p>')

    return HttpResponse('<p class="error">Une erreur est survenue.</p>')

def change_pwd(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseBadRequest()

    if request.method == 'POST':
        old_pwd = request.POST.get('old-pwd')
        new_pwd = request.POST.get('new-pwd')
        confirm_new_pwd = request.POST.get('new-pwd-confirm')

        if old_pwd and new_pwd and confirm_new_pwd:
            if new_pwd == confirm_new_pwd:
                try:
                    validate_password(new_pwd)

                    if request.user.check_password(old_pwd):
                        request.user.set_password(new_pwd)
                        request.user.save()
                        request.user = authenticate(username=request.user.username, password=new_pwd)
                        if request.user: login(request, request.user)
                        return HttpResponse('<p class="success">Le mot de passe a bien été modifié. Rechargement de la page...</p>')

                    else:
                        return HttpResponseBadRequest('<p class="error">L\'ancien mot de passe est incorrect.</p>')

                except Exception as e:
                    return HttpResponseBadRequest('<p class="error">Le mot de passe n\'est pas assez sécurisé.</p>')

            return HttpResponseBadRequest('<p class="error">Les mots de passe ne correspondent pas.</p>')

    return HttpResponseBadRequest('<p class="error">Une erreur est survenue. Vérifiez que vous avez bien rempli tous les champs.</p>')

def friends(request: HttpRequest) -> HttpResponse:
    listfriends = request.user.friends.all()
    return render(request, 'friends.html', {'friends': listfriends})

def delete_friend(request: HttpRequest, friend_id: int) -> HttpResponse:
    friend = request.user.friends.get(id=friend_id)
    request.user.friends.remove(friend)
    return HttpResponse('')

def search_user(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        query = request.POST.get('username')
        if query:
            users = CustomUser.objects.filter(username__icontains = query).order_by('username')[:6]
            return render(request, 'reusable/search_user.html', {'users': users})
        
        return render(request, 'reusable/search_user.html', {'users': []})

    return HttpResponseBadRequest('')
