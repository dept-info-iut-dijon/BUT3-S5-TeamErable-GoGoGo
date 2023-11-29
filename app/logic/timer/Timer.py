from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Timer(ABC):

    @abstractmethod
    def __init__(self):
        pass
    
    def start(self):
        '''Lance le timer'''
        self.started = True

    def isStarted(self):
        return self.started

    @abstractmethod
    def make_move(self):
        '''Retire le temps mis pour faire le coup du timer'''
        pass
    """
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