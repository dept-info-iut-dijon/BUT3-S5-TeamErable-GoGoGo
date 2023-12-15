from .game_configuration_struct import GameConfigurationStruct
from ...models.game_configuration import GameConfiguration

def game_configuration_to_game_configuration_struct(game_configuration: GameConfiguration) -> GameConfigurationStruct:
    '''Fonction permettant de convertir un GameConfiguration en GameConfigurationStruct

    Args:
        game_configuration (GameConfiguration): Le GameConfiguration à convertir

    Returns:
        GameConfigurationStruct: Le GameConfigurationStruct
    '''
    return GameConfigurationStruct(
        is_private = game_configuration.is_private,
        ranked = game_configuration.ranked,
        map_size = game_configuration.map_size,
        counting_method = game_configuration.counting_method,
        byo_yomi = game_configuration.byo_yomi,
        clock_type = game_configuration.clock_type,
        time_clock = game_configuration.clock_value,
        komi = game_configuration.komi,
        handicap = game_configuration.handicap,
    )
