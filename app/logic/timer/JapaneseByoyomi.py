from . import TimerBase
from .TimerFactory import TimerFactory
from .. import Board, Tile
from datetime import datetime, timedelta

class JapaneseByoyomi(TimerBase):
	key: str = 'japanese'

	def __init__(self, board: Board, byo_yomi: int, time: timedelta, player_time: dict[Tile, timedelta] | None) -> None:
		super().__init__(board, byo_yomi, time, player_time)
		# self._initialize_separate_timer(timer_data)
		# self.byo_yomi = timer_data['byo_yomi']
		# self.new_time = None
		# self.initial_time = None
		# if 'initial_time' in timer_data.keys():
		# 	self.initial_time = timer_data['initial_time']

	def set_move(self) -> None:
		'''Definit le timestamp du coup pour le calcul du temps.'''
		self.new_time = datetime.now().timestamp()
		if self.initial_time == None:
			self.initial_time = self.new_time

	def make_move(self, player:Tile) -> bool:
		is_game_over = False
		if self.main_time_black <= 0 and player == Tile.Black:
			is_game_over = self._evaluate_byoyomi()
		elif self.main_time_white <= 0 and player == Tile.White:
			is_game_over = self._evaluate_byoyomi()
		else:
			self._main_time(player)
		self.initial_time = self.new_time
		print("White:"+str(self.main_time_white))
		print("Black"+str(self.main_time_black))
		return is_game_over

	def _evaluate_byoyomi(self) -> bool:
		'''
        Evalue si la periode de byo-yomi est ecoulee.

        Returns :
            bool: True si la periode de byo-yomi est ecoulee, False sinon.
        '''
		res = False
		if int(self.new_time - self.initial_time) > int(self.byo_yomi):
			res = True
		return res
			

	def _main_time(self, player:Tile):
		'''
        Met a jour le temps principal en fonction du coup du joueur.

        Args :
            player (Tile): Le joueur effectuant le coup (Noir ou Blanc).
        '''
		if(player == Tile.White):
			self.main_time_white -= self.new_time - self.initial_time
		else:
			self.main_time_black -= self.new_time - self.initial_time
		

	def get_initial_time(self) -> float:
		return self.initial_time

	def get_separate_timers(self) -> tuple[int, int]:
		return (self.main_time_black, self.main_time_white)


TimerFactory().register(JapaneseByoyomi)
