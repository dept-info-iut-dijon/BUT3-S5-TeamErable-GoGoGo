from .JapaneseByoyomi import JapaneseByoyomi
from .ChineseByoyomi import ChineseByoyomi
from .Timer import Timer

class TimerFactory:
	@staticmethod
	def create_timer(timer_data: dict):
		ret = None
		match timer_data['type']:
			case "japanese":
				ret = TimerFactory.create_japanese_byoyomi(timer_data)
			case "chinese":
				ret = TimerFactory.create_chinese_byoyomi(timer_data)
			case _:
				pass
		return ret

	@staticmethod
	def create_japanese_byoyomi(timer_data: dict)->JapaneseByoyomi:
		return JapaneseByoyomi(timer_data)

	@staticmethod
	def create_chinese_byoyomi(timer_data: dict)->ChineseByoyomi:
		return ChineseByoyomi(timer_data)
