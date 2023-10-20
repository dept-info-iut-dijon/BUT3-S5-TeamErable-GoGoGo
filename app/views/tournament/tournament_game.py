from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def tournament_game(request: HttpRequest, idplayer1:int, idplayer2: int) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    
    game = Game.objects.create(
                name = name,
                description = description,
                start_date = datetime.now(),
                duration = 0,
                done = False,
                tournament = None,
                player1 = request.user,
                player2 = None,
                code = code
            )

    return render(request, 'tournament/tournament.html')