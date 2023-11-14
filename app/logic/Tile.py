from enum import Enum

class Tile(Enum):
    '''Tuile du plateau de jeu.'''

    White = '⚪'
    Black = '⚫'

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def from_str(value: str) -> 'Tile | None':
        '''Convertit une chaîne de caractères en une tuile.

        Args:
            value (str): Chaîne de caractères à convertir.

        Returns:
            Tile | None: Tuile correspondante ou None si la chaîne n'est pas valide.
        '''
        for tile in Tile:
            if str(tile) == value:
                return tile
        return None

    def next(self) -> 'Tile':
        '''Renvoie la tuile suivante.

        Returns:
            Tile: Tuile suivante.
        '''
        l = list(Tile)
        return l[(l.index(self) + 1) % len(l)]
