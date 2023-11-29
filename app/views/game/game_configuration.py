from .game_configuration_struct import GameConfigurationStruct
from ...models.game_configuration import GameConfiguration
from ...http import HttpResponseNotifError

def _split_value(value : str) -> int:
    '''Sépare une chaine de caractères en nombre de secondes
    
    Args:
        value (str): Chaine de caractères (HH:MM:SS)
        
    Returns:
        int: Nombre de secondes correspondant au temps de jeu
    '''
    list_str = value.split(':')
    ret = int(list_str[0]) * 3600 + int(list_str[1]) * 60 + int(list_str[2])
    return ret

def _convert(map_size : str, komi : str, handicap : str) -> dict:
    '''Convertit une chaine de caractères en dictionnaire
    
    Args:
        map_size (str): Taille de la carte
        komi (str): Komi
        handicap (str): Handicap

    Returns:
        dict: Dictionnaire contenant la taille de la carte, le komi et le handicap
    '''
    ret = None
    try: 
        map_size = int(map_size)
        komi = float(komi)
        handicap = int(handicap)
        ret = {'map_size' : map_size, 'komi' : komi, 'handicap' : handicap}
    except:
        return HttpResponseNotifError('Erreur : Valeur invalide')
    return ret

def create_game_config(game_configuration : GameConfigurationStruct) -> GameConfiguration:
    '''Créer une configuration de partie

    Args:
        game_configuration (GameConfigurationStruct): Configuration de la partie

    Returns:
        GameConfiguration: Configuration de la partie
    '''
    convert_value = _convert(game_configuration.map_size, game_configuration.komi, game_configuration.handicap)

    configuration = GameConfiguration.objects.create(
        is_private = game_configuration.is_private,
        ranked = game_configuration.ranked,
        map_size = convert_value['map_size'],
        komi = convert_value['komi'],
        counting_method = game_configuration.counting_method,
        byo_yomi = game_configuration.byo_yomi,
        clock_type = game_configuration.clock_type,
        clock_value = _split_value(game_configuration.time_clock),
        handicap = convert_value['handicap']
    )

    return configuration