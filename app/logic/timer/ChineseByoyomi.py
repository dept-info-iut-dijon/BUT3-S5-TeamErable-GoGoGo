from . import Timer
from ...models.game_configuration import GameConfiguration

class ChineseByoyomi(Timer):
	def __init__(self, timer_data: dict):
		self.main_time = timer_data['clock_value']
		self.byo_yomi = timer_data['byo_yomi']
		self.started = False

	def make_move(self):
		self.main_time-=1;