from enum import Enum



class Tile(Enum):
    White = 'W'
    Black = 'B'

    def __str__(self) -> str:
        return str(self.value)



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
        s = ''
        for y in range(self._size):
            for x in range(self._size):
                s += self._board[y][x] if self._board[y][x] else ' '
            s += '\n'
        return s
