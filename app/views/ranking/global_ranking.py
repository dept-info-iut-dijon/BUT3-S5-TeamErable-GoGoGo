from django.db.models import Count, F, Q, ExpressionWrapper, fields, Case, When, FloatField,OuterRef, Subquery
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.db.models.functions import Coalesce
from django.db import models
from ...models import CustomUser, Game,GameParticipate
from ..decorators import login_required, request_type, RequestType
from .ranking_struct import RankingStruct

@login_required
@request_type(RequestType.GET)
def global_ranking(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de classement global

    Args:
        request (HttpRequest): Requete HTTP

    Returns:
        HttpResponse: Reponse HTTP de la page de classement global
    '''
    users = list(CustomUser.objects.all())
    global_ranking = _get_top_rank(users, 1)

    friends = list(request.user.friends.all())
    friends.append(request.user)
    friends_ranking = _get_top_rank(friends, 1)

    return render(request, 'ranking/global.html', {'user': request.user, 'friends_ranked': friends_ranking, 
        'top_ranked': global_ranking})

def _get_top_rank(user_range: list[CustomUser], limit:int) -> list[RankingStruct]:
    '''
        Permet d'obtenir un classement selon une certaine liste d'utilisateurs

        Args:
            user_range (list[CustomUser]): Liste des utilisateurs concernes
            limit (int): position du dernier elment affiche

        Returns:
            list[RankingStruct]: le classement 
    '''
    #Constante correspondant au nombre d'elements du classement affiches simultanement
    LIMIT_RANGE = 20
    ranking:list[CustomUser] = []
    
    ranked_game_participate_ids = Game.objects.filter(
        game_configuration__ranked=True
    ).values('game_participate_id')

    game_participates = list(GameParticipate.objects.filter(
            Q(player1__in=user_range) | Q(player2__in=user_range),
            id_game_participate__in=Subquery(ranked_game_participate_ids)
    ).values())

    history = _get_history(user_range, game_participates)
    history = _merge_player_history(history)
    ranking = _get_as_ranking(history)
    ranking = sorted(ranking, key=_sorting_key, reverse=True)[limit*LIMIT_RANGE-LIMIT_RANGE:limit*LIMIT_RANGE]

    return ranking

def _get_history(user_range:list[CustomUser],game_participates: list[dict])->list[(int, bool)]:
    '''
        Permet d'obtenir l'historique par joueur des parties classees
        
        Args:
            user_range (list[CustomUser]): liste des utilisateurs concernees par le classement
            game_participates (list[dict]): liste des parties classes
        
        Returns:
            list[(int, bool)]: l'historique par joueur des parties classees
    '''
    history = []
    for game_participate in game_participates:
        if not (game_participate['score_player1'] == 0 and game_participate['score_player2'] == 0):
            is_winner = game_participate['score_player1'] > game_participate['score_player2']
            player1 = CustomUser.objects.filter(id=game_participate['player1_id']).first()
            player2 = CustomUser.objects.filter(id=game_participate['player2_id']).first()
            if(player1 in user_range):
                history.append((game_participate['player1_id'], is_winner))
            if(player2 in user_range):
                history.append((game_participate['player2_id'], not is_winner))
    return history

def _merge_player_history(history: list[(int, bool)])->dict:
    '''
        Trie l'historique des parties classees par joueur

        Args:
            history(list[(int, bool)]): liste des victoires et defaites de chaque joueur concerne

        Returns:
            dict: historiques de chaque joueur (nb total parties et victoires)
    '''
    merged_history = {}
    for record in history:
        if record[0] not in merged_history:
            merged_history[record[0]] = [int(record[1]), 1]
        else:
            merged_history[record[0]][0] += int(record[1])
            merged_history[record[0]][1] += 1
    return merged_history

def _get_as_ranking(history: dict)-> list[RankingStruct]:
    '''
        Obtient la liste des structure de ranking pour chaque joueur

        Args:
            history (dict): dictionaire des statistiques de chaque joueurs

        Returns:
            list[RankingStruct]: liste des lignes du classement
    '''
    ranking = []
    for id_player,player_data in history.items():
        ranking.append(RankingStruct(
            CustomUser.objects.filter(id=id_player).first(),
            "1er dan",
            1400,
            player_data[1],
            player_data[0],
            player_data[1]-player_data[0],
            player_data[0]*100/player_data[1]
        ))

    return ranking

def _sorting_key(ranking_data:RankingStruct)->tuple:
    '''
        Fonction servant de cle pour la comparaison de tri d'une liste de RankingStruct

        Args:
            ranking_data (RankingStruct): donnes a trier

        Returns:
            tuple: cle de tri
    '''
    return (ranking_data.taux_victory, ranking_data.nb_games)