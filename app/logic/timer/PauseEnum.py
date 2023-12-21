from enum import Enum
from typing_extensions import Literal

class PauseEnum(Enum):
    Not = 0
    Normal = 1
    Forced = 2

    def export(self) -> int:
        return self.value

    def __bool__(self) -> Literal[True]:
        return self.value != 0
