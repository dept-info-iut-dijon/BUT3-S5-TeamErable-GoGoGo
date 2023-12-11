from .TimerBase import TimerBase
from .TimerFactory import TimerFactory
from ...logic import Board, Tile
from datetime import datetime, timedelta

class JapaneseByoyomi(TimerBase):
	key: str = 'japanese'

	def __init__(
        self,
        board: Board,
        byo_yomi: int,
        initial_time: timedelta,
        player_time: dict[Tile, timedelta] | None,
        last_action_time: datetime | None,
        is_paused: bool = False,
        ask_pause: list[Tile] = [],
        ask_resume: list[Tile] = [],
        timer_offset: timedelta = timedelta(seconds = 0)
    ) -> None:
		super().__init__(board, byo_yomi, initial_time, player_time, last_action_time, is_paused, ask_pause, ask_resume, timer_offset)


	def copy(self) -> TimerBase:
		return JapaneseByoyomi(
			self._board,
			self._byo_yomi,
			self._initial_time,
			self._player_time,
			self._last_action_time,
			self._is_paused,
			self._ask_pause,
			self._ask_resume,
			self._timer_offset
		)


	def play(self, tile: Tile) -> None:
		delta = datetime.now() - self._last_action_time
		self._player_time[tile] -= delta

		if self._player_time[tile] < timedelta(seconds = self.byo_yomi):
			self._player_time[tile] = timedelta(seconds = self.byo_yomi)

		self.update_last_action_time()
		self.reset_timer_offset()


TimerFactory().register(JapaneseByoyomi)
