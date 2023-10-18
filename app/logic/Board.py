from enum import Enum



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



class Board:
    def __init__(self, size: int) -> None:
        self._size = size
        self._board: list[list[Tile | None]] = [[None for _ in range(size)] for _ in range(size)]

    @property
    def size(self) -> int:
        return self._size
    
    @property
    def raw(self) -> list:
        return self._board
    
    def get(self, x: int, y: int) -> Tile | None:
        return self._board[y][x]
    
    def set(self, x: int, y: int, value: str) -> None:
        self._board[y][x] = value

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
