from django.http import HttpRequest
from django.shortcuts import redirect
from functools import wraps
from typing import Callable

def login_required(f: Callable) -> Callable:
    '''Décorateur permettant de valider si l'utilisateur est connecté

    Args:
        f (Callable): Fonction à décorer

    Returns:
        Callable: Fonction décorée
    '''
    @wraps(f)
    def wrapper(request: HttpRequest, *args, **kwargs) -> Callable:
        return f(request, *args, **kwargs) if request.user.is_authenticated else redirect('/login')
    return wrapper


def logout_required(f: Callable) -> Callable:
    '''Décorateur permettant de valider si l'utilisateur est connecté

    Args:
        f (Callable): Fonction à décorer

    Returns:
        Callable: Fonction décorée
    '''
    @wraps(f)
    def wrapper(request: HttpRequest, *args, **kwargs) -> Callable:
        return f(request, *args, **kwargs) if not request.user.is_authenticated else redirect('/')
    return wrapper
