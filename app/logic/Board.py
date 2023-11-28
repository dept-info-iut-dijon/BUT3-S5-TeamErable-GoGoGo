from plum import dispatch as overload
from .Vector2 import Vector2
from .Tile import Tile
from .Island import Island
from ..exceptions import InvalidMoveException
from .GoConstants import GoConstants
from .RuleBase import RuleBase
from .RuleFactory import RuleFactory


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
        self._size = Vector2(size, size)
        self._rule: RuleBase = rule_cls(self)
        self._board: list[list[Tile | None]] = [[None for _ in range(self._size.x)] for _ in range(self._size.y)]
        self._current_player = Tile.White

        self._eaten_tiles = {}
        for tile in Tile:
            self._eaten_tiles[tile] = 0

        self._komi = komi

        self._ended: bool = False
        self._skip_list: list[Tile] = []


    @property
    def size(self) -> Vector2:
        return self._size


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
    def raw(self) -> list[list[Tile | None]]:
        l = []

        for y in range(self._size.y):
            l.append([])
            for x in range(self._size.x):
                match self.get(Vector2(x, y)):
                    case Tile.White:
                        l[y].append('white')

                    case Tile.Black:
                        l[y].append('black')

                    case _:
                        l[y].append(None)

        return l


    def get(self, coords: Vector2) -> Tile | None:
        '''Renvoie la tuile aux coordonnées spécifiées.

        Args:
            coords (Vector2): Coordonnées de la tuile.

        Raises:
            ValueError: Si les coordonnées sont en dehors du plateau.

        Returns:
            Tile | None: _description_
        '''
        if self.is_outside(coords): raise ValueError('Les coordonnées sont en dehors du plateau.')
        return self._board[coords.y][coords.x]


    def set(self, coords: Vector2, value: Tile) -> None:
        '''Définit la tuile aux coordonnées spécifiées.

        Args:
            coords (Vector2): Coordonnées de la tuile.
            value (Tile): Valeur de la tuile.

        Raises:
            ValueError: Si les coordonnées sont en dehors du plateau.
        '''
        if self.is_outside(coords): raise ValueError('Les coordonnées sont en dehors du plateau.')
        self._board[coords.y][coords.x] = value


    def is_outside(self, coords: Vector2) -> bool:
        return coords.x < 0 or coords.x >= self._size.x or coords.y < 0 or coords.y >= self._size.y


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
        if self.is_outside(coords): raise InvalidMoveException('Impossible de jouer ici, les coordonnées sont en dehors du plateau.')
        if self.get(coords) is not None: raise InvalidMoveException('Impossible de jouer ici, la case est déjà occupée.')

        ret: dict[Tile, list[Vector2]] = {t: [] for t in Tile} | {None: []}

        self.set(coords, tile)

        has_eaten = False

        for neightbor in self.get_neighbors(coords):
            if self.is_outside(neightbor): continue

            island = self.get_island_from_coords(neightbor)
            if island is None: continue

            if self.is_island_surronded(island):
                has_eaten = True
                for c in island.coords:
                    self.set(c, None)
                    ret[None].append(c)
                    self._eaten_tiles[tile.next] += 1

        if not has_eaten:
            island = self.get_island_from_coords(coords)
            if self.is_island_surronded(island):
                if GoConstants.AllowPlayInDeadZones:
                    for c in island.coords:
                        self.set(c, None)
                        ret[None].append(c)
                        self._eaten_tiles[tile.next] += 1

                else:
                    self.set(coords, None)
                    raise InvalidMoveException('Impossible de jouer ici, l\'île serait entourée.')

        if self.get(coords) is not None:
            ret[tile].append(coords)

        self._current_player = tile.next
        self._skip_list = []

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

        if set(self._skip_list) == set(Tile):
            self.end_game()


    def end_game(self) -> None:
        '''Termine la partie.'''
        if self._ended: raise InvalidMoveException('La partie est déjà terminée.')
        self._ended = True


    def get_neighbors(self, coords: Vector2) -> list[Vector2]:
        '''Renvoie les coordonnées des voisins.

        Args:
            coords (Vector2): Coordonnées de la tuile.

        Returns:
            list[Vector2]: Coordonnées des voisins.
        '''
        return [coords + c for c in GoConstants.Neighbors if not self.is_outside(coords + c)]


    def get_islands(self) -> tuple[Island]:
        '''Renvoie les îles de tuiles.

        Returns:
            tuple[Island]: Îles de tuiles.
        '''
        grid = [[False for _ in range(self._size.x)] for _ in range(self._size.y)]
        islands = []

        for y in range(self._size.y):
            for x in range(self._size.x):
                if grid[y][x]: continue

                tile = self._board[y][x]
                if tile is None: continue

                island = Island(tile, Vector2(x, y))
                grid[y][x] = True

                stack = [Vector2(x, y)]
                while stack:
                    coords = stack.pop()
                    for neighbor in self.get_neighbors(coords):
                        if grid[neighbor.y][neighbor.x]: continue

                        if self._board[neighbor.y][neighbor.x] == tile:
                            island.add(neighbor)
                            grid[neighbor.y][neighbor.x] = True
                            stack.append(neighbor)

                islands.append(island)

        return tuple(islands)


    def get_island_from_coords(self, coords: Vector2) -> Island | None:
        '''Renvoie l'île de tuiles aux coordonnées spécifiées.

        Args:
            coords (Vector2): Coordonnées de la tuile.

        Returns:
            Island | None: Île de tuiles.
        '''
        if self.is_outside(coords): return None

        tile = self.get(coords)
        if tile is None: return None

        for island in self.get_islands():
            if island.tile == tile and coords in island.coords:
                return island
            
        return None


    def is_island_surronded(self, island: Island) -> bool:
        '''Vérifie si l'île de tuiles est entourée de tuiles adverses.

        Args:
            island (Island): Île de tuiles.

        Returns:
            bool: True si l'île est entourée, False sinon.
        '''
        enemy_tile = island.tile.next

        for coords in island.get_arround_tiles():
            if self.is_outside(coords): continue

            tile: Tile = self.get(coords)
            if tile != enemy_tile: return False

        return True


    def __str__(self) -> str:
        s = '╔' + '═' * (self._size.x * 3) + '╗\n'
        for y in range(self._size.y):
            s += '║'
            for x in range(self._size.x):
                s += (str(self._board[y][x]) if self._board[y][x] else '➕') + ' '
            s += '║\n'
        return s + '╚' + '═' * (self._size.x * 3) + '╝'

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


    def get_raw_territory(self, tile: Tile) -> tuple[Island]:
        '''Renvoie le territoire brut de tuiles du joueur donné. -> Ne prend pas en compte les autres joueurs.

        Args:
            tile (Tile): Tuile du joueur. Renvoie les territoires du joueur si spécifié.

        Returns:
            tuple[Island]: Territoire de tuiles.
        '''
        territories = []

        board = [[(self.get(Vector2(x, y)) == tile) for x in range(self._size.x)] for y in range(self._size.y)]

        def next_tile():
            for y in range(self._size.y):
                for x in range(self._size.x):
                    if board[y][x]: continue

                    return Vector2(x, y)

            return None

        while pos := next_tile():
            group: list[Vector2] = []

            stack = [pos]
            while stack:
                coords = stack.pop()
                group.append(coords)
                board[coords.y][coords.x] = True

                for neighbor in self.get_neighbors(coords):
                    if self.is_outside(neighbor): continue

                    if not board[neighbor.y][neighbor.x]:
                        board[neighbor.y][neighbor.x] = True
                        stack.append(neighbor)

            territories.append(Island(tile, *(group)))

        return tuple(territories)


    def get_raw_territories(self) -> dict[Tile, tuple[Island]]:
        '''Renvoie les territoires bruts de tuiles.

        Returns:
            dict[Tile, tuple[Island]]: Territoires bruts de tuiles.
        '''
        territories = {}

        for tile in Tile:
            territories[tile] = self.get_raw_territory(tile)

        return territories


    def get_territories(self) -> dict[Tile, tuple[Island]]:
        '''Renvoie les territoires de tuiles.

        Returns:
            tuple[Island]: Territoires de tuiles.
        '''

        raw_territories: dict[Tile, tuple[Island]] = self.get_raw_territories()
        territories: dict[Tile, list[Island]] = {}

        for tile in Tile:
            territories[tile] = list(raw_territories[tile])

        for tile in Tile:
            for other_territory in territories[tile.next].copy():
                for this_territory in territories[tile].copy():
                    if other_territory.contains(this_territory) and other_territory in territories[tile.next]:
                        territories[tile.next].remove(other_territory)

        return {tile: tuple(territories[tile]) for tile in Tile}


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
        self._size = Vector2(*data['size'])
        self._board = [
            [
                Tile.from_value(b[y][x]) if b[y][x] else None
                for x in range(self._size.x)
            ]
            for y in range(self._size.y)
        ]
        self._current_player = Tile.from_value(data['current-player'])
        self._eaten_tiles = {
            Tile.from_value(k): v
            for k, v in data['eaten-tiles'].items()
        }
        self._rule = RuleFactory().get(data['rule'])
        self._komi = data['komi']
        self._ended = data['ended']
        self._skip_list = [Tile.from_value(t) for t in data['skip-list']]


    def export(self) -> dict:
        '''Exporte le plateau de jeu.

        Returns:
            dict: Données du plateau.
        '''

        return {
            'board': [
                [
                    str(self._board[y][x]) if self._board[y][x] else None
                    for x in range(self._size.x)
                ]
                for y in range(self._size.y)
            ],
            'size': [self._size.x, self._size.y],
            'current-player': str(self._current_player),
            'eaten-tiles': {
                str(tile): self._eaten_tiles[tile]
                for tile in Tile
            },
            'rule': self._rule.key,
            'komi': self._komi,
            'ended': self._ended,
            'skip-list': [str(tile) for tile in self._skip_list],
            # 'history': [],
        }


    def get_corner_points(self, coords: Vector2) -> list[Vector2]:
        corners = []

        if not self.is_outside(Vector2(coords.x - 1, coords.y - 1)): corners.append(Vector2(coords.x - 1, coords.y - 1))
        if not self.is_outside(Vector2(coords.x + 1, coords.y - 1)): corners.append(Vector2(coords.x + 1, coords.y - 1))

        if not self.is_outside(Vector2(coords.x - 1, coords.y + 1)): corners.append(Vector2(coords.x - 1, coords.y + 1))
        if not self.is_outside(Vector2(coords.x + 1, coords.y + 1)): corners.append(Vector2(coords.x + 1, coords.y + 1))

        return corners


    def get_group_and_neighbors(self, starting_point: Vector2) -> tuple[list[Vector2], list[Vector2]]:
        starting_points = [starting_point]
        return self.get_group_and_neighbors_from_points(starting_points)


    def get_group_and_neighbors_from_points(self, starting_points: list[Vector2]) -> tuple[list[Vector2], list[Vector2]]:
        tocheck = starting_points.copy()
        neighbors = []
        visited = [[False for _ in range(self._size.x)] for _ in range(self._size.y)]
        matching_value = self.get(starting_points[0])

        group = []

        while tocheck:
            p = tocheck.pop(0)
            if self.get(p) == matching_value:
                group.append(p)
                for neighbor in self.get_neighbors(p):
                    if visited[neighbor.y][neighbor.x]: continue

                    visited[neighbor.y][neighbor.x] = True
                    tocheck.append(neighbor)

            else:
                neighbors.append(p)

        return group, neighbors


    def count_equal(self, group: list[Vector2], value: Tile | None) -> int:
        ret = 0
        for coords in group:
            if self.get(coords) == value:
                ret += 1

        return ret


    def all_equal_to(self, group: list[Vector2], value: Tile | None) -> bool:
        for coords in group:
            if self.get(coords) != value:
                return False

        return True


    def get_min_liberties_of_surrounding_groups(self, coords: Vector2) -> int:
        neighbors = self.get_neighbors(coords)

        ret = 99999

        for neighbor in neighbors:
            group, group_neighbors = self.get_group_and_neighbors(neighbor)

            liberties = self.count_equal(group_neighbors, None)
            ret = min(ret, liberties)

        return ret


    def get_false_eyes(self) -> tuple[Vector2]:
        false_eyes: list[Vector2] = []

        for y in range(self._size.y):
            for x in range(self._size.x):
                coords = Vector2(x, y)
                if self.get(coords) is not None: continue

                neighbors = self.get_neighbors(coords)
                corners = self.get_corner_points(coords)

                if self.get_min_liberties_of_surrounding_groups(coords) > 1: continue

                if self.all_equal_to(neighbors, Tile.Black) and self.count_equal(corners, Tile.White) >= (len(corners) >> 1):
                    false_eyes.append(coords)

                elif self.all_equal_to(neighbors, Tile.White) and self.count_equal(corners, Tile.Black) >= (len(corners) >> 1):
                    false_eyes.append(coords)

        return false_eyes


    def copy(self) -> 'Board':
        '''Copie le plateau de jeu.

        Returns:
            Board: Copie du plateau de jeu.
        '''

        b = Board(self._size.x, self._komi, self._rule.__class__)
        b._board = [row.copy() for row in self._board]
        b._current_player = self._current_player
        b._eaten_tiles = self._eaten_tiles.copy()
        b._ended = self._ended
        b._skip_list = self._skip_list.copy()

        return b
