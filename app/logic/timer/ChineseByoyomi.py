from . import Timer

class ChineseByoyomi(Timer):
	def __init__(self, timer_data: dict) -> None:
		self.main_time = timer_data['clock_value']
		self.byo_yomi = timer_data['byo_yomi']
		self.started = False

	def set_move(self) -> None:
		raise NotImplementedError()

	def make_move(self) -> bool:
		self.main_time -= 1

	def get_initial_time(self) -> float:
		raise NotImplementedError()

	def get_separate_timers(self) -> tuple[int, int]:
		raise NotImplementedError()
