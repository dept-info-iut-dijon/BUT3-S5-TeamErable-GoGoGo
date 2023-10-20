class Vector2:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self._x + other._x, self._y + other._y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self._x - other._x, self._y - other._y)

    def __str__(self) -> str:
        return f'Vector2({self._x}, {self._y})'
