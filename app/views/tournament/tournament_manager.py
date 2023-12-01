from django.http import FileResponse, HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from ...models.tournament import Tournament, ParticipateTournament
from ...models.game import Game
from django.contrib.auth import get_user_model
import datetime, os, json
from ...logic import Board
from app.models import Game
from app.models import CustomUser
from ..decorators import login_required
from ...http import HttpResponseNotifError

def has_game_happened(tournament_games:list[Game], player1:CustomUser, player2:CustomUser)->Game:
    '''
        Verifie si la partie a eut lieu
        Args:
            tournament_games (List[Game]): liste des parties liees au tournois
            player1 (CustomUser): le joueur 1 de la partie concernee
            player2 (CustomUser): le joueur 2 de la partie concernee

        Returns:
            Game: la partie ou None si elle n'existe pas
    '''
    ret = None
    for game in tournament_games:
        if (game.player1 == player1 and game.player2 == player2) or (game.player1 == player2 and game.player2 == player1):
            ret = game
    return ret

"""def create_tournament_game(tournament, player1, player2):
    '''
        Cree une partie liee au tournois
    '''
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
        b = Board(size) # TODO: A corriger
        json.dump(b.export(), f)
    curr_game.move_list = file
    curr_game.save()"""

@login_required
def tournament_manager(request: HttpRequest, id: int) -> HttpResponse:
    '''
        Affiche la page de gestion du tournois
        
        Args:
            request (HttpRequest): Requete http
            id (int): id du tournois

        Returns:
            HttpResponse: Reponse Http de la page demandee
    '''
    tournament = get_object_or_404(Tournament, id=id)
    user = get_organisator_user(tournament)
    participants = get_tournament_participants(tournament)
    games = Game.objects.filter(tournament=tournament)
    tournament_games = generate_tournament_tree(participants, games)
    context = {
        'tournament': tournament,
        'organisator': user,
        'tree': tournament_games,
        'in_tournament': request.user in participants,
        'ongoing': tournament.ongoing()
    }

    return render(request, 'tournament/tournament_manager.html', context)

def get_organisator_user(tournament: Tournament)->CustomUser:
    '''
        Permet d'obtenir l'organisateur du tournois
        Args:
            tournament (Tournament): le tournois

        Returns:
            CustomUser: L'organisateur du tournois
    '''
    try:
        user = get_user_model().objects.get(username=tournament.organisator)
    except get_user_model().DoesNotExist:
        user = None
    return user

def get_tournament_participants(tournament:Tournament)->list[CustomUser]:
    '''
        Permet d'obtenir la liste des participants du tournois
        Args:
            tournament (Tournament): le tournois

        Returns:
            list[CustomUser]: la liste des user participants
    '''
    participate = ParticipateTournament.objects.filter(tournament=tournament)
    participants = [entry.person for entry in participate]
    return participants

def generate_tournament_tree(participants:list[CustomUser], games:list[Game])->list[list]:
    '''
        Genere l'arbre de tournois
        Args:
            participants (list[CustomUser]): la liste des participants
            games (list[Game]): la liste des parties liees au tournois

        Returns:
            list[list]: la liste des rounds
    '''
    tournament_games = []
    current_round = [(participants[i - 1], participants[i]) for i in range(1, len(participants), 2)]
    lone_member = get_lone_member(participants)
    round_iter = 0

    while len(current_round) != 0:
        tournament_games.append([])
        next_round = []

        for match in current_round:
            curr_game = has_game_happened(games, match[0], match[1])
            player1, player2 = get_player_status(match[0], match[1], curr_game)
            next_round.append(curr_game.winner) if curr_game else next_round.append(None)
            tournament_games[round_iter].append((player1, player2, curr_game))

        lone_member = handle_lone_member(lone_member, next_round, current_round)
        current_round = create_next_round(next_round, lone_member)
        round_iter += 1
    return tournament_games

def get_lone_member(participants:list[CustomUser])->CustomUser:
    '''
        Permet d'obtenir un eventuel participant impaire

        Args:
            participants (CustomUser): liste des participants 

        Returns:
            CustomUser: Le participant impaire
    '''
    lone_member = None
    if len(participants) % 2 == 1:
        lone_member = participants[-1]
    return lone_member

def handle_lone_member(lone_member:CustomUser, next_round:list[CustomUser], current_round:list)->CustomUser:
    '''
        Fait la gestion du membre impaire
        
        Args:
            lone_member (CustomUser): l'utilisateur impaire
            next_round (list[CustomUser]): liste des utilisateur du round suivant
            current_round (list): liste des matchs du round actuel

        Returns:
            CustomUser: l'utilisateur impaire
    '''
    if lone_member:
        if len(current_round) == 1:
            current_round = [(lone_member, next_round[0])]
            lone_member = None
        else:
            current_round = [(next_round[i - 1], next_round[i]) for i in range(3, len(next_round), 2)]
            current_round.insert(0, (lone_member, next_round[0]))
            lone_member = next_round[1]
    return lone_member

def create_next_round(next_round:list[CustomUser], lone_member:CustomUser)->list:
    '''
        Cree la liste des mathcs du prochain round

        Args:
            next_round (list[CustomUser]): liste de gagnants du round
            lone_member (CustomUser): l'utilisateur impaire

        Returns:
            list: liste des matchs du prochain round

    '''
    if lone_member:
        current_round = [(next_round[i - 1], next_round[i]) for i in range(1, len(next_round), 2)]
    else:
        current_round = [(next_round[i - 1], next_round[i]) for i in range(1, len(next_round), 2)]
    return current_round

def get_player_status(player1:CustomUser, player2:CustomUser, curr_game:Game)-> bool:
    '''
        Permet d'obtenir le status gagnant d'un joueur par rapport a une partie

        Args:
            player1 (CustomUser): le joueur 1
            player2 (CustomUser): le joueur 2
            curr_game (Game): la partie 
        
        Returns:
            bool: status des joueurs 1 et 2
    '''
    player1_status = [player1, False]
    player2_status = [player2, False]

    if curr_game:
        if str(curr_game.winner) == str(player1.username):
            player1_status[1] = True
        elif str(curr_game.winner) == str(player2.username):
            player2_status[1] = True

    return player1_status, player2_status
    

@login_required
def tournament_join(request: HttpRequest, id_tournament:int) -> HttpResponse:

    tournament = get_object_or_404(Tournament, id=id_tournament)

    if tournament.ongoing() == True: 
        return HttpResponseNotifError('Les inscription pour ce tournois sont terminees')

    if len(ParticipateTournament.objects.filter(person=request.user, tournament=tournament).all()) < 1:
        link = ParticipateTournament.objects.create(
                person = request.user,
                tournament = tournament,
                win = False,
            )
        return HttpResponse('''
            <script>
                    window.location.reload();
            </script>
            ''')
    else:
        return HttpResponseNotifError('Vous participez deja au tournois')

@login_required
def tournament_player_list(request: HttpRequest) -> HttpResponse:

    if request.method == 'GET':
        if (id_tournament := request.GET.get('id')) is None: return HttpResponseNotifError('Une erreur est survenue')
        try:
            tournament = Tournament.objects.get(id = id_tournament)
            listplayers = CustomUser.objects.filter(participatetournament__tournament__id = id_tournament).all()
            return render(request, 'reusable/tournament_player_list.html', {'players': listplayers, 'tournament_unstarted': (not tournament.ongoing()) and tournament.creator.id == request.user.id})
        
        except: return HttpResponseNotifError('Une erreur est survenue')

    return HttpResponseBadRequest()
