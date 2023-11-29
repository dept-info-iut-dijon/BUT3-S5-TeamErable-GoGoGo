from . import Timer
from datetime import datetime
import math

class JapaneseByoyomi(Timer):
	def __init__(self, timer_data: dict):
		self.main_time = timer_data['clock_value']
		self.byo_yomi = timer_data['byo_yomi']
		self.started = False
		self.initial_time:float = datetime.now().timestamp()
		print("init")

	def make_move(self):
		print("move")
		new_time = datetime.now().timestamp()
		print(new_time)
		print(self.initial_time)
		#self.main_time -= (new_time.timestamp() - self.initial_time.timestamp())
		self.initial_time = new_time
		#print(self.main_time)