from datetime import timedelta
from ...logic import Tile, Vector2

class WatchMove:
    def __init__(self, from_: timedelta, to_: timedelta, player: Tile, player_time: timedelta, eaten_tiles: dict[Tile, int], changes: dict[Tile, tuple[Vector2]]) -> None:
        self._from = from_
        self._to = to_
        self._player = player
        self._player_time = player_time
        self._eaten_tiles = eaten_tiles
        self._changes = changes


    @property
    def from_(self) -> timedelta:
        return self._from

    @property
    def to_(self) -> timedelta:
        return self._to

    @property
    def player(self) -> Tile:
        return self._player

    @property
    def player_time(self) -> timedelta:
        return self._player_time

    @property
    def eaten_tiles(self) -> dict[Tile, int]:
        return self._eaten_tiles

    @property
    def changes(self) -> dict[Tile, tuple[Vector2]]:
        return self._changes


    def time_overlap(self, timestamp: timedelta) -> bool:
        return self._from <= timestamp <= self._to
