class TileColor:
    def __init__(self, value: str, color: str) -> None:
        self._value = value
        self._color = color

    @property
    def value(self) -> str:
        return self._value

    @property
    def color(self) -> str:
        return self._color

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()
