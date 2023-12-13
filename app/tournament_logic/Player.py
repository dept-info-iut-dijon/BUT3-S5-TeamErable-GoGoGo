class Player:
    def __init__(self, id: int) -> None:
        self._id = id


    @property
    def id(self) -> int:
        return self._id


    def __str__(self) -> str:
        return f'{__class__.__name__}(id = {self._id})'


    def __repr__(self) -> str:
        return str(self)


    def __eq__(self, other: object) -> bool:
        return isinstance(other, Player) and self._id == other._id
