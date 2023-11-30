from .JapaneseByoyomi import JapaneseByoyomi
from .ChineseByoyomi import ChineseByoyomi
from .Timer import Timer

class TimerFactory:
	@staticmethod
	def createTimer(timer_data: dict):
		ret = None
		match timer_data['type']:
			case "japanese":
				ret = TimerFactory.createJapaneseByoyomi(timer_data)
			case "chinese":
				ret = TimerFactory.createChineseByoyomi(timer_data)
			case _:
				pass
		return ret

	@staticmethod
	def createJapaneseByoyomi(timer_data: dict)->JapaneseByoyomi:
		return JapaneseByoyomi(timer_data)

	@staticmethod
	def createChineseByoyomi(timer_data: dict)->ChineseByoyomi:
		return ChineseByoyomi(timer_data)