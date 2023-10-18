from django.http import FileResponse, HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from ...models.tournament import Tournament, Participate
from ...models.game import Game
from django.contrib.auth import get_user_model


def has_game_happened(tournament_games, player1, player2):
    for game in tournament_games:
        if (game.player1 == player1 and game.player2 == player2) or (game.player1 == player2 and game.player2 == player1):
            return game
    return None

def tournament_manager(request: HttpRequest, id:int) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    
    tournament = get_object_or_404(Tournament, id=id)
    try:
        user = get_user_model().objects.get(username=tournament.organisator)
    except get_user_model().DoesNotExist:
        user = None
    
    participate = Participate.objects.filter(tournament=tournament)
    participants = [entry.person for entry in participate]
    games = Game.objects.filter(tournament=tournament)

    tournament_games = []

    current_round = [(participants[i], participants[i + 1]) for i in range(0, len(participants), 2)]
    round_iter = 0
    while (len(current_round)!=0):
        #Ajout du round
        tournament_games.append([])
        next_round = []
        #Ajout des match du round en cours
        for match in current_round:
            curr_game = has_game_happened(games, match[0], match[1])
            player1 = [match[0],False]
            player2 = [match[1],False]
            #Modification du status du gagnant
            if curr_game != None:
                if curr_game.winner == player1:
                    player1[1] = True
                else:
                    player2[1] = True  
                next_round.append(curr_game.winner)
            else:
                next_round.append(None)
            tournament_games[round_iter].append((player1,player2))
        #Creation du round suivant
        if len(current_round) == 1 :
            current_round = []
        else:
            current_round = [(next_round[i], next_round[i + 1]) for i in range(0, len(next_round), 2)]
        round_iter+=1
    context = {
        'tournament': tournament,
        'organisator': user,
        'tree': tournament_games,
    }

    return render(request, 'tournament/tournament_manager.html', context)