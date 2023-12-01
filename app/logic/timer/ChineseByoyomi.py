from . import TimerBase
from .TimerFactory import TimerFactory
from .. import Board, Tile
from datetime import timedelta

class ChineseByoyomi(TimerBase):
	key: str = 'chinese'

	def __init__(self, board: Board, byo_yomi: int, time: timedelta, player_time: dict[Tile, timedelta] | None) -> None:
		super().__init__(board, byo_yomi, time, player_time)
		# self.main_time = timer_data['clock_value']
		# self.byo_yomi = timer_data['byo_yomi']
		self.started = False

	def set_move(self) -> None:
		raise NotImplementedError()

	def make_move(self) -> bool:
		self.main_time -= 1

	def get_initial_time(self) -> float:
		raise NotImplementedError()

	def get_separate_timers(self) -> tuple[int, int]:
		raise NotImplementedError()


TimerFactory().register(ChineseByoyomi)
