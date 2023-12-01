from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from ..Tile import Tile

class Timer(ABC):

    @abstractmethod
    def __init__(self, timer_data: dict) -> None:
        '''
        Methode du constructeur pour le minuteur

        Args :
            timer_data (dict): Dictionnaire contenant les donnees de configuration du minuteur.
        '''
        pass
    

    @abstractmethod
    def set_move(self) -> None:
        '''Sauvegarde le temps du nouveau placement'''
        pass


    @abstractmethod
    def make_move(self, player: Tile) -> bool:
        '''
        Gere le calcul du temps pour chaque coup.

        Args :
            player (Tile): Le joueur effectuant le coup (Noir ou Blanc).

        Returns :
            bool: True si la partie est terminee, False sinon.
        '''
        pass

    @abstractmethod
    def get_initial_time(self) -> float:
        '''
            Permet d'obtenir le temps depuis le dernier coup

            Returns:
                float: le temps depuis le dernier coup
        '''
        pass

    @abstractmethod
    def get_separate_timers(self) -> tuple[int, int]:
        '''
            Permet d'obtenir l'etat des timers separes

            Returns:
                (int, int): Tuple contenant l'etat des timers blanc et noir
        '''
        pass
