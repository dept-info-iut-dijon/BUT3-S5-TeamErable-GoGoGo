from enum import Enum
from .Vector2 import Vector2



class Tile(Enum):
    White = 'O'
    Black = 'X'

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def from_str(value: str) -> 'Tile | None':
        for tile in Tile:
            if str(tile) == value:
                return tile
        return None

    def next(self) -> 'Tile':
        l = list(Tile)
        return l[(l.index(self) + 1) % len(l)]



class Board:
    def __init__(self, size: int) -> None:
        self._size = size
        self._board: list[list[Tile | None]] = [[None for _ in range(size)] for _ in range(size)]
        self._current_player = Tile.White

    @property
    def size(self) -> int:
        return self._size

    @property
    def raw(self) -> list:
        return self._board

    def get(self, x: int, y: int) -> Tile | None:
        if x < 0 or x >= self._size or y < 0 or y >= self._size: raise Exception('Les coordonnées sont en dehors du plateau.')
        return self._board[y][x]

    def set(self, coords: Vector2, value: str) -> None:
        if coords.x < 0 or coords.x >= self._size or coords.y < 0 or coords.y >= self._size: raise Exception('Les coordonnées sont en dehors du plateau.')
        self._board[coords.y][coords.x] = value

    def play(self, coords: Vector2, tile: Tile) -> tuple[tuple[int, int], Tile]:
        if self._current_player != tile: raise Exception('Ce n\'est pas à vous de jouer.')
        if self._board[coords.y][coords.x] is not None: raise Exception('Impossible de jouer ici, la case est déjà occupée.')

        self.set(coords, tile)
        # TODO: check if the move is valid

        self._current_player = tile.next()

    def _detect_group(self, coords: Vector2, tile: Tile) -> list[tuple[int, int]]:
        pass

    def __str__(self) -> str:
        s = '╔' + '═' * (self._size * 2 + 1) + '╗\n'
        for y in range(self._size):
            s += '║ '
            for x in range(self._size):
                s += (str(self._board[y][x]) if self._board[y][x] else ' ') + ' '
            s += '║\n'
        return s + '╚' + '═' * (self._size * 2 + 1) + '╝'

    def load(self, data: dict) -> None:
        b = data['board']
        self._board = [
            [
                Tile.from_str(b[y][x]) if b[y][x] else None
                for x in range(self._size)
            ]
            for y in range(self._size)
        ]

    def export(self) -> dict:
        return {
            'board': [
                [
                    str(self._board[y][x]) if self._board[y][x] else None
                    for x in range(self._size)
                ]
                for y in range(self._size)
            ],
            'history': [],
        }
