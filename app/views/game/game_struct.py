from dataclasses import dataclass
from ...http import verify_post
from django.http import HttpRequest
from typing import Union
from .game_configuration_struct import GameConfigurationStruct

@dataclass
class GameStruct:
    name : str
    description : str
    game_configuration : GameConfigurationStruct

    @classmethod
    def verify_game(cls, request: HttpRequest) -> Union["GameStruct", Exception]:
        '''Fonction permettant de valider les informations de la partie et de la renvoyer

        Args:
            request (HttpRequest): Requête HTTP

        Returns:
            GameStruct: La partie ou l'exception
        '''
        ret = None
        try: 
            game_config = GameConfigurationStruct.verify_game_config(request)

            ret = cls(
                name = verify_post(request, 'game-name', 'Le nom de la partie est vide.'),
                description = verify_post(request, 'game-desc', 'La description de la partie est vide.'),
                game_configuration = game_config
            )

        except Exception as e:
            ret = e
        
        return ret
    
    def __str__(self):
        return (f"GameStruct(name={self.name}, "
                f"description={self.description}) ")