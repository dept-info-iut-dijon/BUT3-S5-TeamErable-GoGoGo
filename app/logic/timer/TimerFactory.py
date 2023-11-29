from .JapaneseByoyomi import JapaneseByoyomi
from .ChineseByoyomi import ChineseByoyomi
from .Timer import Timer
from ...models.game_configuration import GameConfiguration

class TimerFactory:
	@staticmethod
	def createTimer(timer_type:str):
		ret = None
		match timer_type:
			case "japanese":
				ret = TimerFactory.createJapaneseByoyomi()
			case "chinese":
				ret = TimerFactory.createChineseByoyomi()
			case _:
				pass
		return ret

	@staticmethod
	def createJapaneseByoyomi()->JapaneseByoyomi:
		return JapaneseByoyomi()

	@staticmethod
	def createChineseByoyomi()->ChineseByoyomi:
		return ChineseByoyomi()