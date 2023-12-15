from enum import Enum, auto

class GoRank(Enum):
    TRENTE_KYU = auto()
    VINGT_NEUF_KYU = auto()
    VINGT_HUIT_KYU = auto()
    VINGT_SEPT_KYU = auto()
    VINGT_SIX_KYU = auto()
    VINGT_CINQ_KYU = auto()
    VINGT_QUATRE_KYU = auto()
    VINGT_TROIS_KYU = auto()
    VINGT_DEUX_KYU = auto()
    VINGT_ET_UN_KYU = auto()
    VINGT_KYU = auto()
    DIX_NEUF_KYU = auto()
    DIX_HUIT_KYU = auto()
    DIX_SEPT_KYU = auto()
    SEIZE_KYU = auto()
    QUINZE_KYU = auto()
    QUATORZE_KYU = auto()
    TREIZE_KYU = auto()
    DOUZE_KYU = auto()
    ONZE_KYU = auto()
    DIX_KYU = auto()
    NEUF_KYU = auto()
    HUIT_KYU = auto()
    SEPT_KYU = auto()
    SIX_KYU = auto()
    CINQ_KYU = auto()
    QUATRE_KYU = auto()
    TROIS_KYU = auto()
    DEUX_KYU = auto()
    UN_KYU = auto()

    PREMIER_DAN = auto()
    DEUXIEME_DAN = auto()
    TROISIEME_DAN = auto()
    QUATRIEME_DAN = auto()
    CINQUIEME_DAN = auto()
    SIXIEME_DAN = auto()
    SEPTIEME_DAN = auto()
    HUITIEME_DAN = auto()
    NEUVIEME_DAN = auto()

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
        rank_number = self.name.split('_')[0]
        if 'KYU' in self.name:
            return f"{rank_number}ème Kyu"
        elif 'DAN' in self.name:
            return f"{rank_number}er Dan"