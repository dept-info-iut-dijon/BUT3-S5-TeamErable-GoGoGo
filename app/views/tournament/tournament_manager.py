from django.http import FileResponse, HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from ...models.tournament import Tournament, Participate
from ...models.game import Game
from django.contrib.auth import get_user_model
import datetime, os, json
from ...logic import Board
from app.models import Game

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

    #liste des matchs pour le premier round
    current_round = [(participants[i-1], participants[i]) for i in range(1, len(participants), 2)]
    #gestion du participant impair
    lone_member = None
    if len(participants) % 2 == 1:
        lone_member = participants[len(participants)-1]
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
                if str(curr_game.winner) == str(player1[0].username):
                    player1[1] = True
                elif str(curr_game.winner) == str(player2[0].username):
                    player2[1] = True
                next_round.append(curr_game.winner)
            else:
                next_round.append(None)
                curr_game = Game.objects.create(
                    name = str(player1[0]) + " VS " + str(player2[0]),
                    description = "Match du tournois " + str(tournament.name) + " oposant " + str(player1[0]) + " et " + str(player2[0]),
                    start_date = datetime.datetime.now(),
                    duration = 0,
                    done = False,
                    tournament = tournament,
                    player1 = player1[0],
                    player2 = player2[0],
                    code = tournament.code,
                    is_private = False,
                )
                file = f'dynamic/games/{curr_game.id_game:X}.json'
                size = 6

                if not os.path.exists('dynamic/games'): os.makedirs('dynamic/games')
                with open(file, 'w') as f:
                    b = Board(size)
                    json.dump(b.export(), f)

                curr_game.move_list = file
                curr_game.save()
            tournament_games[round_iter].append((player1,player2,curr_game))
        #Creation du round suivant
        if lone_member != None:
            if len(current_round) == 1:
                current_round = [(lone_member, next_round[0])]
                lone_member = None
            else:
                current_round = []
                current_round = [(next_round[i-1], next_round[i]) for i in range(3, len(next_round), 2)]
                current_round.insert(0,(lone_member, next_round[0]))
                lone_member = next_round[1]
        else:
            if len(current_round) == 1 :
                current_round = []
            else:
                current_round = [(next_round[i-1], next_round[i]) for i in range(1, len(next_round), 2)]
        round_iter+=1

    print(tournament.ongoing())
    context = {
        'tournament': tournament,
        'organisator': user,
        'tree': tournament_games,
        'in_tournament': request.user in participants,
        'ongoing': tournament.ongoing()
    }

    return render(request, 'tournament/tournament_manager.html', context)

def tournament_join(request: HttpRequest, id_tournament:int) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    tournament = get_object_or_404(Tournament, id=id_tournament)

    if tournament.ongoing() == True: 
        return HttpResponseBadRequest('<p class="error">Les inscription pour ce tournois sont terminees</p>') 

    if len(Participate.objects.filter(person=request.user, tournament=tournament).all()) < 1:
        link = Participate.objects.create(
                person = request.user,
                tournament = tournament,
                win = False,
            )
        return HttpResponse(f'<p class="success">Vous avez rejoint le tournois.</p>')
    else:
        return HttpResponseBadRequest('<p class="error">Vous participez deja au tournois</p>') 

    print(id_tournament)

    