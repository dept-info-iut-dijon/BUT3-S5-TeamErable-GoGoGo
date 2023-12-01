from . import Timer
from ..Tile import Tile
from datetime import datetime
import math

class JapaneseByoyomi(Timer):
	def __init__(self, timer_data: dict) -> None:
		self._initialize_separate_timer(timer_data)
		self.byo_yomi = timer_data['byo_yomi']
		self.new_time = None
		self.initial_time = None
		if 'initial_time' in timer_data.keys():
			self.initial_time = timer_data['initial_time']

	def _initialize_separate_timer(self, timer_data: dict) -> None:
		'''
        Methode auxiliaire pour initialiser les minuteurs separes.

        Args :
            timer_data (dict): Dictionnaire contenant les donnees de configuration du minuteur.
        '''
		if 'separate_timer' in timer_data.keys():
			self.main_time_black = timer_data['separate_timer'][0]
			self.main_time_white = timer_data['separate_timer'][1]
		else:
			self.main_time_black = timer_data['clock_value']
			self.main_time_white = timer_data['clock_value']
		

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
	