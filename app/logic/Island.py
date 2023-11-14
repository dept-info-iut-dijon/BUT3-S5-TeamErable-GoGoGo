from .Tile import Tile
from .Vector2 import Vector2
from .GoConstants import GoConstants

class Island:
    '''Île de tuiles.'''

    def __init__(self, tile: Tile, *coords: Vector2) -> None:
        '''Constructeur.

        Args:
            tile (Tile): Tuile de l'île.
            *coords (Vector2): Coordonnées des tuiles.
        '''
        self._tile = tile
        self._coords = tuple(coords)


    @property
    def tile(self) -> Tile:
        return self._tile
    
    @property
    def coords(self) -> tuple[Vector2]:
        return self._coords


    def add(self, coord: Vector2) -> None:
        '''Ajoute une coordonnée.

        Args:
            coord (Vector2): Coordonnée à ajouter.
        '''
        self._coords += (coord,)


    def __eq__(self, __value: object) -> bool:
        '''Compare deux îles de tuiles.

        Args:
            __value (object): Île de tuiles à comparer.

        Returns:
            bool: True si les îles sont égaux, False sinon.
        '''
        if not isinstance(__value, Island): return False

        return self._tile == __value._tile and set(self._coords) == set(__value._coords)


    def __str__(self) -> str:
        return f'Island({self._tile}, {self._coords})'

    def __repr__(self) -> str:
        return str(self)


    def get_arround_tiles(self) -> tuple[Vector2]:
        '''Renvoie les coordonnées des tuiles adjacentes.

        Returns:
            tuple[Vector2]: Coordonnées des tuiles adjacentes.
        '''

        arround_tiles = []
        for coord in self._coords:
            for neighbor in GoConstants.Neighbors:
                arrond_tile = coord + neighbor

                if not arrond_tile in self._coords:
                    arround_tiles.append(arrond_tile)

        return tuple(arround_tiles)
