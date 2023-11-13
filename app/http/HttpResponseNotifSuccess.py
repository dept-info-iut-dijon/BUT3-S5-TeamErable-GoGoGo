from typing import Any
from django.http import HttpResponse

class HttpResponseNotifSuccess(HttpResponse):
    '''Class représentant une réponse avec une notification de succès'''

    def __init__(self, content: str, *args: Any, **kwargs: Any) -> None:
        '''Constructeur de HttpResponseNotifSuccess

        Args:
            content (str): Contenu de la réponse
        '''
        super().__init__(f'<p class="success">{content}<p>', *args, **kwargs)
