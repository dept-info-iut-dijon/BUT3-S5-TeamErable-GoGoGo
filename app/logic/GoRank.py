from enum import Enum, auto

class GoRank(Enum):
    _30_KYU = auto()
    _29_KYU = auto()
    _28_KYU = auto()
    _27_KYU = auto()
    _26_KYU = auto()
    _25_KYU = auto()
    _24_KYU = auto()
    _23_KYU = auto()
    _22_KYU = auto()
    _21_KYU = auto()
    _20_KYU = auto()
    _19_KYU = auto()
    _18_KYU = auto()
    _17_KYU = auto()
    _16_KYU = auto()
    _15_KYU = auto()
    _14_KYU = auto()
    _13_KYU = auto()
    _12_KYU = auto()
    _11_KYU = auto()
    _10_KYU = auto()
    _9_KYU = auto()
    _8_KYU = auto()
    _7_KYU = auto()
    _6_KYU = auto()
    _5_KYU = auto()
    _4_KYU = auto()
    _3_KYU = auto()
    _2_KYU = auto()
    _1_KYU = auto()

    _1_DAN = auto()
    _2_DAN = auto()
    _3_DAN = auto()
    _4_DAN = auto()
    _5_DAN = auto()
    _6_DAN = auto()
    _7_DAN = auto()
    _8_DAN = auto()
    _9_DAN = auto()

    """@classmethod
    def from_string(cls, rank_str):
        rank_number, rank_type = rank_str.split('ème ')
        rank_number = int(rank_number)

        if rank_type == 'Kyu':
            return cls[f'NEUVIEME_DAN']
        elif rank_type == 'Dan':
            return cls[f'NEUVIEME_DAN']
        else:
            raise ValueError("Invalid rank type")
        return cls[f'NEUVIEME_DAN']"""

    def __str__(self):
        rank_number = self.name.split('_')[1]
        suffix = "ème"
        if rank_number == 1:
            suffix = "er"
        if 'KYU' in self.name:
            return f"{rank_number}{suffix} Kyu"
        elif 'DAN' in self.name:
            return f"{rank_number}{suffix} Dan"