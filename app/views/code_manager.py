import random
import string
from django.db.models import QuerySet
from ..models.game import Game

# Classe qui s'occupe de la gestion des codes unique des parties et tournois
class CodeManager:
    
    def generate_unique_code(self) -> str:
        '''Methode generant un code unique aleatoire

        Returns:
            str: Un code unique

        '''
        code = None
        while (code is None or Game.objects.filter(code=code, done=False).exists()):
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        return code
