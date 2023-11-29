from plum import dispatch as overload
from .Vector2 import Vector2
from .Tile import Tile
from .Island import Island
from ..exceptions import InvalidMoveException
from .GoConstants import GoConstants
from .RuleBase import RuleBase
from .RuleFactory import RuleFactory
from .Grid import Grid


class Board:
    '''Plateau de jeu.'''

    @overload
    def __init__(self, data: dict) -> None:
        '''Initialise un plateau de jeu.

        Args:
            data (dict): Données du plateau.
        '''
        self.load(data)


    @overload
    def __init__(self, size: int, komi: float, rule_cls: type[RuleBase]) -> None:
        '''Initialise un plateau de jeu.

        Args:
            size (int): Taille du plateau.
            komi (float): Komi.
            rule_cls (type[RuleBase]): Classe de la règle.
        '''
        self._grid = Grid(size)
        self._rule: RuleBase = rule_cls(self)
        self._current_player = Tile.White

        self._eaten_tiles = {}
        for tile in Tile:
            self._eaten_tiles[tile] = 0

        self._komi = komi

        self._ended: bool = False
        self._skip_list: list[Tile] = []
        self._illegal_moves: list[Vector2] = []
        self._history: list[Vector2] = []


    @property
    def size(self) -> Vector2:
        return self._grid.size

    @property
    def width(self) -> int:
        return self._grid.width

    @property
    def height(self) -> int:
        return self._grid.height

    @property
    def grid(self) -> Grid:
        return self._grid

    @property
    def current_player(self) -> Tile:
        return self._current_player

    @property
    def ended(self) -> bool:
        return self._ended

    @property
    def komi(self) -> float:
        return self._komi

    @property
    def history(self) -> list[Vector2]:
        return self._history.copy()
    
    @property
    def skip_list(self) -> list[Tile]:
        return self._skip_list.copy()
    
    @property
    def illegal_moves(self) -> list[Vector2]:
        return self._illegal_moves.copy()


    def get(self, coords: Vector2) -> Tile:
        '''Renvoie la tuile à la position donnée.

        Args:
            coords (Vector2): Coordonnées.

        Returns:
            Tile: Tuile.
        '''
        return self._grid.get(coords)


    def set(self, coords: Vector2, tile: Tile) -> None:
        '''Modifie la tuile à la position donnée.

        Args:
            coords (Vector2): Coordonnées.
            tile (Tile): Tuile.
        '''
        self._grid.set(coords, tile)


    def play(self, coords: Vector2, tile: Tile) -> dict[Tile, tuple[Vector2]]:
        '''Joue un coup.

        Args:
            coords (Vector2): Coordonnées du coup.
            tile (Tile): Tuile du joueur.

        Raises:
            InvalidMoveException: Si la partie est terminée.
            InvalidMoveException: Si le joueur n'est pas le joueur courant.
            InvalidMoveException: Si la case est déjà occupée.
            InvalidMoveException: Si l'île serait entourée (Si le joueur n'est pas autorisé à jouer dans les zones mortes).
        '''
        if self._ended: raise InvalidMoveException('La partie est terminée.')
        if self._current_player != tile: raise InvalidMoveException('Ce n\'est pas à vous de jouer.')
        if self._grid.is_outside(coords): raise InvalidMoveException('Impossible de jouer ici, les coordonnées sont en dehors du plateau.')
        if self.get(coords) is not None: raise InvalidMoveException('Impossible de jouer ici, la case est déjà occupée.')
        if any(coords == pos for pos in self._illegal_moves): raise InvalidMoveException('Impossible de jouer ici, la case s\'est déjà retrouvée entourée lors du dernier tour.')

        ret: dict[Tile, list[Vector2]] = {t: [] for t in Tile} | {None: []}

        self.set(coords, tile)

        has_eaten = False

        for neightbor in self.get_neighbors(coords):
            if self._grid.is_outside(neightbor): continue

            island = self._grid.get_island_from_coords(neightbor)
            if island is None: continue

            if self._grid.is_island_surronded(island):
                has_eaten = True
                for c in island.coords:
                    self._eaten_tiles[self.get(c).next] += 1
                    self.set(c, None)
                    ret[None].append(c)

        if not has_eaten:
            island = self._grid.get_island_from_coords(coords)
            if self._grid.is_island_surronded(island):
                if GoConstants.AllowPlayInDeadZones:
                    for c in island.coords:
                        self._eaten_tiles[self.get(c)] += 1
                        self.set(c, None)
                        ret[None].append(c)

                else:
                    self.set(coords, None)
                    raise InvalidMoveException('Impossible de jouer ici, l\'île serait entourée.')

        if self.get(coords) is not None:
            ret[tile].append(coords)

        self._history.append(coords)
        self._current_player = tile.next
        self._skip_list = []

        if len(ret[None]) == 1:
            self._illegal_moves = [ret[None][0]]

        else:
            self._illegal_moves = []

        return ret


    def play_skip(self, tile: Tile) -> None:
        '''Passe le tour.

        Args:
            tile (Tile): Tuile du joueur.

        Raises:
            InvalidMoveException: Si la partie est terminée.
            InvalidMoveException: Si le joueur n'est pas le joueur courant.
        '''
        if self._ended: raise InvalidMoveException('La partie est terminée.')
        if self._current_player != tile: raise InvalidMoveException('Ce n\'est pas à vous de jouer.')

        self._skip_list.append(tile)

        self._current_player = tile.next
        self._history.append(None)
        self._illegal_moves = []

        if set(self._skip_list) == set(Tile):
            self.end_game()


    def end_game(self) -> None:
        '''Termine la partie.'''
        if self._ended: raise InvalidMoveException('La partie est déjà terminée.')
        self._ended = True


    def __str__(self) -> str:
        return str(self._grid)

    def __repr__(self) -> str:
        return str(self)


    def get_eaten_tiles(self, tile: Tile) -> int:
        '''Renvoie le nombre de tuiles mangées par le joueur.

        Args:
            tile (Tile): Tuile du joueur.

        Returns:
            int: Nombre de tuiles mangées.
        '''
        return self._eaten_tiles[tile]


    def is_player_turn(self, tile: Tile) -> bool:
        '''Vérifie si c'est au joueur de jouer.

        Args:
            tile (Tile): Tuile du joueur.

        Returns:
            bool: True si c'est au joueur de jouer, False sinon.
        '''
        return self._current_player == tile


    def load(self, data: dict) -> None:
        '''Charge un plateau de jeu.

        Args:
            data (dict): Données du plateau.
        '''

        b = data['board']
        self.size = Vector2(*data.get('size', [len(b[0]), len(b)])[:2])
        self._grid = Grid.from_list([
            [
                Tile.from_value(b[y][x]) if b[y][x] else None
                for x in range(self.size.x)
            ]
            for y in range(self.size.y)
        ])
        self._current_player = Tile.from_value(data.get('current-player', Tile.White))
        self._eaten_tiles = {
            Tile.from_value(k): v
            for k, v in data.get('eaten-tiles', {t.value.value: 0 for t in Tile}).items()
        }
        self._rule = RuleFactory().get(data.get('rule', 'chinese'))
        self._komi = data.get('komi', 0.5)
        self._ended = data.get('ended', False)
        self._skip_list = [Tile.from_value(t) for t in data.get('skip-list', [])]
        self._illegal_moves = [
            Vector2(*pos) if pos else None
            for pos in data.get('illegal-moves', [])
        ]
        self._history = [
            Vector2(*pos) if pos else None
            for pos in data.get('history', [])
        ]


    def export(self) -> dict:
        '''Exporte le plateau de jeu.

        Returns:
            dict: Données du plateau.
        '''

        return {
            'board': [
                [
                    str(self.get(Vector2(x, y))) if self.get(Vector2(x, y)) else None
                    for x in range(self.size.x)
                ]
                for y in range(self.size.y)
            ],
            'size': [self.size.x, self.size.y],
            'current-player': str(self._current_player),
            'eaten-tiles': {
                str(tile): self._eaten_tiles[tile]
                for tile in Tile
            },
            'rule': self._rule.key,
            'komi': self._komi,
            'ended': self._ended,
            'skip-list': [str(tile) for tile in self._skip_list],
            'illegal-moves': [[pos.x, pos.y] if pos else None for pos in self._illegal_moves],
            'history': [[pos.x, pos.y] if pos else None for pos in self._history],
        }


    def copy(self) -> 'Board':
        '''Copie le plateau de jeu.

        Returns:
            Board: Copie du plateau de jeu.
        '''

        b = Board(self.size.x, self._komi, self._rule.__class__)
        b._grid = Grid.from_list([row.copy() for row in self._grid])
        b._current_player = self._current_player
        b._eaten_tiles = self._eaten_tiles.copy()
        b._ended = self._ended
        b._skip_list = self._skip_list.copy()
        b._illegal_moves = [pos.copy() for pos in self._illegal_moves]
        b._history = [pos.copy() for pos in self._history]

        return b


    def get_false_eyes(self) -> list[Vector2]:
        '''Renvoie les positions des yeux faux.

        Returns:
            list[Vector2]: Positions des yeux faux.
        '''
        return self._grid.get_false_eyes()
    

    def get_territories(self) -> dict[Tile, list[Island]]:
        '''Renvoie les territoires.

        Returns:
            dict[Tile, list[Island]]: Territoires.
        '''
        return self._grid.get_territories()


    def get_neighbors(self, coords: Vector2) -> list[Vector2]:
        '''Renvoie les voisins d'une case.

        Args:
            coords (Vector2): Coordonnées.

        Returns:
            list[Vector2]: Voisins.
        '''
        return self._grid.get_neighbors(coords)
