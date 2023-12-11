from .RuleBase import RuleBase
from ...utils import Singleton

class RuleFactory(metaclass = Singleton):
    '''Fabrique de règles de jeu.'''

    def __init__(self) -> None:
        '''Initialise la fabrique de règles de jeu.'''
        self._rules = {}

    def register(self, rule_cls: type[RuleBase]) -> None:
        '''Enregistre une règle de jeu.

        Args:
            rule_cls (type[RuleBase]): Classe de la règle de jeu.
        '''
        self._rules[rule_cls.key] = rule_cls

    def get(self, key: str) -> type[RuleBase]:
        '''Renvoie une règle de jeu.

        Args:
            key (str): Clé de la règle de jeu.

        Returns:
            type[RuleBase]: Classe de la règle de jeu.
        '''
        return self._rules[key]
