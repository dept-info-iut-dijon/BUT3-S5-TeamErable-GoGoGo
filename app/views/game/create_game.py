from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ...models.game import Game
from ...models.game_configuration import GameConfiguration
from ...models.game_participate import GameParticipate
from datetime import datetime
import random, string, os, json
from ...logic import Board, RuleFactory
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from ..code_manager import CodeManager


def _delete_current_games(user):
    '''Fonction supprimant les parties en cours d'un utilisateur
    
    Args:
        user (CustomUser): l'utilisateur concerné
    '''
    current_games = Game.objects.filter(game_participate__in = GameParticipate.objects.filter(player1 = user)).filter(done=False).all()
    for game in current_games:
        if game.move_list:
            try:
                os.remove(game.move_list.path)
            except:
                pass
        game.delete()

def _create_new_game(name, description, is_private, user, code, map_size, counting_method, byo_yomi, clock_type, clock_value, komi, handicap):
    '''Fonction permettant de creer une nouvelle partie
    
    Args:
        name (str): le nom de la partie
        description (str): la description de la partie
        is_private (bool): boolean indiquant si la partie est privee
        user (CustomUser): l'utilisateur concerné
    '''

    list_str = clock_value.split(':')
    clock_value = int(list_str[0]) * 3600 + int(list_str[1]) * 60 + int(list_str[2])

    configuration = GameConfiguration.objects.create(
        is_private = is_private,
        map_size = map_size,
        komi = komi,
        counting_method = counting_method,
        clock_type = clock_type,
        clock_value = clock_value,
        byo_yomi = byo_yomi,
        handicap = handicap,
    )

    participate = GameParticipate.objects.create(
        player1 = user,
        player2 = None,
        score_player1 = 0,
        score_player2 = 0
    )
    
    game = Game.objects.create(
        name = name,
        description = description,
        code = code,
        start_date = datetime.now(),
        duration = 0,
        done = False,
        tournament = None,
        game_configuration = configuration,
        game_participate = participate,
        )
    
    file = f'dynamic/games/{game.id_game:X}.json'

    if not os.path.exists('dynamic/games'):
        os.makedirs('dynamic/games')
    with open(file, 'w') as f:
        b = Board(map_size,RuleFactory().get(counting_method))
        json.dump(b.export(), f)

    game.move_list = file
    game.save()

    return game


@login_required
@request_type(RequestType.GET, RequestType.POST)
def create_game(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de création de partie

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de création de partie
    '''
    ret: HttpResponse = HttpResponseNotifError('Erreur lors de la création de la partie')
    if request.method == RequestType.POST.value:
        if (name := request.POST.get('game-name')) is None: ret = HttpResponseNotifError('Erreur : Le nom de la partie est vide')
        elif (is_private := bool(request.POST.get('game-private', False))) is None: ret = HttpResponseNotifError('Erreur : Le statut de la partie n\'est pas défini')
        elif (description := request.POST.get('game-desc')) is None: ret = HttpResponseNotifError('Erreur : La description de la partie est vide')
        elif (map_size := request.POST.get('map-size')) is None: ret = HttpResponseNotifError('Erreur : La taille de la carte est vide')
        elif (counting_method := request.POST.get('counting-method')) is None: ret = HttpResponseNotifError('Erreur : La methode de comptage est vide')
        elif (byo_yomi := request.POST.get('byo-yomi')) is None: ret = HttpResponseNotifError('Erreur : Le byo-yomi est vide')
        elif (clock_type := request.POST.get('clock-type')) is None: ret = HttpResponseNotifError('Erreur : Le temps de la partie est vide ')
        elif (time_clock := request.POST.get('time-clock')) is None: ret = HttpResponseNotifError('Erreur : Le temps de la partie est vide')
        elif (komi := request.POST.get('komi')) is None: ret = HttpResponseNotifError('Erreur : La valeur de komi est vide')
        elif (handicap := request.POST.get('handicap')) is None: ret = HttpResponseNotifError('Erreur : La valeur de handicap est vide')


        else:
            try: 
                map_size = int(map_size)
                komi = float(komi)
                handicap = int(handicap)
            except:
                return HttpResponseNotifError('Erreur : Valeur invalide')
            
            code_manager = CodeManager()
            code = code_manager.generate_unique_code()

            _delete_current_games(request.user)
            
            game = _create_new_game(name, description, is_private, request.user, code, map_size, counting_method, byo_yomi, clock_type, time_clock, komi, handicap)
            
            ret = HttpResponse(f'/game?id={game.id_game}')
                

    elif request.method == RequestType.GET.value:
        ret = render(request, 'game/create_game.html')

    return ret
