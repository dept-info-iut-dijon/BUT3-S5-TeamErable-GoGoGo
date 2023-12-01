from .TimerBase import TimerBase
from .TimerFactory import TimerFactory
from ...logic import Board, Tile
from datetime import datetime, timedelta

class JapaneseByoyomi(TimerBase):
	key: str = 'japanese'

	def __init__(self, board: Board, byo_yomi: int, initial_time: timedelta, player_time: dict[Tile, timedelta] | None, last_action_time: datetime | None) -> None:
		super().__init__(board, byo_yomi, initial_time, player_time, last_action_time)


	def copy(self) -> TimerBase:
		return JapaneseByoyomi(self._board, self._byo_yomi, self._initial_time, self._player_time, self._last_action_time)


	def play(self, tile: Tile) -> None:
		delta = datetime.now() - self._last_action_time
		self._player_time[tile] -= delta
		self.update_last_action_time()
		print(tile, self._player_time[tile])


TimerFactory().register(JapaneseByoyomi)
