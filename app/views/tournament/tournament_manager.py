from django.db.models import Q
from django.http import FileResponse, HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from ...models.tournament import Tournament, ParticipateTournament
from ...models.game import Game
from django.contrib.auth import get_user_model
import datetime, os, json
from ...logic import Board
from app.models import Game, GameParticipate
from app.models import CustomUser
from ..decorators import login_required
from ...http import HttpResponseNotifError

def _has_game_happened(tournament_games:list[Game], player1:CustomUser, player2:CustomUser)->GameParticipate:
    '''
        Verifie si la partie a eut lieu
        Args:
            tournament_games (List[Game]): liste des parties liees au tournois
            player1 (CustomUser): le joueur 1 de la partie concernee
            player2 (CustomUser): le joueur 2 de la partie concernee

        Returns:
            GameParticipate: les lien de participation ou None si elle n'existe pas
    '''
    ret = None

    for game in tournament_games:
        game_participate = GameParticipate.objects.filter(
            Q(id_game_participate=game.game_participate_id) &
            (Q(player1=player1) | Q(player1=player2)) &
            (Q(player2=player1) | Q(player2=player2))
        )
        if game_participate.count() == 1:
            ret = game_participate
            break

    return ret


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
    user = _get_organisator_user(tournament)
    participants = _get_tournament_participants(tournament)
    games = Game.objects.filter(tournament=tournament)
    tournament_games = _generate_tournament_tree(participants, games)
    context = {
        'tournament': tournament,
        'organisator': user,
        'tree': tournament_games,
        'in_tournament': request.user in participants,
        'ongoing': tournament.ongoing()
    }

    return render(request, 'tournament/tournament_manager.html', context)

def _get_organisator_user(tournament: Tournament)->CustomUser:
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

def _get_tournament_participants(tournament:Tournament)->list[CustomUser]:
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

def _generate_tournament_tree(participants:list[CustomUser], games:list[Game])->list[list]:
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
    lone_member = _get_lone_member(participants)
    round_iter = 0

    while len(current_round) != 0:
        tournament_games.append([])
        next_round = []
        if lone_member != None:
            next_round.append(lone_member)

        for match in current_round:
            curr_game_participate = _has_game_happened(games, match[0], match[1])
            winner = _get_winner(match[0], match[1], curr_game_participate)
            if winner != None : 
                next_round.append(match[winner])
            else:
                next_round.append(None)
            tournament_games[round_iter].append((match[0], match[1], winner))

        lone_member = _get_lone_member(next_round)
        current_round = _create_next_round(next_round)
        round_iter += 1
    return tournament_games

def _get_lone_member(participants:list[CustomUser])->CustomUser:
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

def _create_next_round(next_round:list[CustomUser])->list:
    '''
        Cree la liste des mathcs du prochain round

        Args:
            next_round (list[CustomUser]): liste de gagnants du round

        Returns:
            list: liste des matchs du prochain round

    '''

    current_round = [(next_round[i - 1], next_round[i]) for i in range(1, len(next_round), 2)]
        
    return current_round

def _get_winner(player1:CustomUser, player2:CustomUser, curr_game_participate:GameParticipate)-> int:
    '''
        Permet d'obtenir le gagnant d'une partie

        Args:
            player1 (CustomUser): le joueur 1
            player2 (CustomUser): le joueur 2
            curr_game (Game): le lien de participation a la partie 
        
        Returns:
            int: position du gagnant dans l'association (0 ou 1)
    '''
    winner=None

    if curr_game_participate != None and curr_game_participate[0]:
        score_player1 = curr_game_participate[0].score_player1
        score_player2 = curr_game_participate[0].score_player2

        if score_player1 > score_player2:
            winner = 0
        elif score_player2 > score_player1:
            winner = 1

    return winner
    

@login_required
def tournament_join(request: HttpRequest, id_tournament:int) -> HttpResponse:
    '''
        Permet de rejoindre un tournois

        Args:
            request (HttpRequest): Requete Http
            id_tournament (int): id du tournois

        Returns:
            HttpResponse: Reponse Http confirmant ou non que l'on a rejoint le tournois
    '''
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
    '''
        Permet de lister les joueurs du tournois

        Args:
            request (HttpRequest): Requete Http

        Returns:
            HttpResponse: Reponse Http contenant la liste
    '''
    ret = HttpResponseBadRequest()
    if request.method == 'GET':
        if (id_tournament := request.GET.get('id')) is None: return HttpResponseNotifError('Une erreur est survenue')
        try:
            tournament = Tournament.objects.get(id = id_tournament)
            listplayers = CustomUser.objects.filter(participatetournament__tournament__id = id_tournament).all()
            ret = render(request, 'reusable/tournament_player_list.html', {'players': listplayers, 'tournament_unstarted': (not tournament.ongoing()) and tournament.creator.id == request.user.id})
        
        except: ret = HttpResponseNotifError('Une erreur est survenue')

    return ret
