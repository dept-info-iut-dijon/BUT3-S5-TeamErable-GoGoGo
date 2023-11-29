from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Timer(ABC):
    def __init__(self):
        pass
    """"
    @abstractmethod
    def start(self):
        '''
            Initialise et lance le timer
        '''
        pass

    @abstractmethod
    def make_move(self):
        '''
            Deduit le temps mis pour faire le coup du timer
        '''
        pass

    @abstractmethod
    def get_remaining_time(self)->int:
        '''Permet d'obtenir le temps restant au joueur
        Returns:
            int: Nombre de secondes correspondant au temps de jeu
        '''
        pass

    @abstractmethod
    def is_timeout(self):
        pass"""