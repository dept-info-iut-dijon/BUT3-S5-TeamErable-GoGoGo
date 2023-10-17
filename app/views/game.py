from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from app.models import Partie

def game(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    if (game_id := request.GET.get('id')) is None: return HttpResponseRedirect('/')

    game_inst = Partie.objects.get(idPartie = game_id, code = None, termine = False)
    if not game_inst: return HttpResponseRedirect('/')

    if game_inst.joueur1 != request.user and game_inst.joueur2 is None:
        game_inst.joueur2 = request.user
        game_inst.save()

    if game_inst.joueur1 != request.user and game_inst.joueur2 != request.user: return HttpResponseRedirect('/')

    return game_logic(request, game_inst)

def game_code(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    if (game_code := request.GET.get('code')) is None: return HttpResponseRedirect('/')

    game_inst = Partie.objects.get(code = game_code, termine = False)
    if not game_inst: return HttpResponseRedirect('/')

    if game_inst.joueur1 != request.user and game_inst.joueur2 is None:
        game_inst.joueur2 = request.user
        game_inst.save()

    if game_inst.joueur1 != request.user and game_inst.joueur2 != request.user: return HttpResponseRedirect('/')

    return game_logic(request, game_inst)



def game_logic(request: HttpRequest, game: Partie) -> HttpResponse:
    return render(request, 'game.html')
