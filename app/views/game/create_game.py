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
from ...http import verify_post, verify_get


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
        b = Board(map_size,komi,RuleFactory().get(counting_method))
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

        try:
            name = verify_post(request, 'game-name', 'Le nom de la partie est vide.')
            is_private = verify_post(request, 'game-private', 'Le statut de la partie n\'est pas défini.')
            description = verify_post(request, 'game-desc', 'La description de la partie est vide.')
            map_size = verify_post(request, 'map-size', 'La taille de la carte est vide.')
            counting_method = verify_post(request, 'counting-method', 'La methode de comptage est vide.')
            byo_yomi = verify_post(request, 'byo-yomi', 'Le byo-yomi est vide.')
            clock_type = verify_post(request, 'clock-type', 'Le temps de la partie est vide.')
            clock_value = verify_post(request, 'clock-value', 'Le temps de la partie est vide.')
            komi = verify_post(request, 'komi', 'Le komi est vide.')
            handicap = verify_post(request, 'handicap', 'Le handicap est vide.')
        
        except Exception as e:
            return HttpResponseNotifError(str(e))

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
            
            game = _create_new_game(name, description, is_private, request.user, code, map_size, counting_method, byo_yomi, clock_type, clock_value, komi, handicap)
            
            ret = HttpResponse(f'/game?id={game.id_game}')
                

    elif request.method == RequestType.GET.value:
        ret = render(request, 'game/create_game.html')

    return ret
