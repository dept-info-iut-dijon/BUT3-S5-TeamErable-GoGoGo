from django.http import HttpRequest
from django.shortcuts import redirect
from functools import wraps
from typing import Callable

def login_required(f: Callable) -> Callable:
    '''Decorator to check if the user is logged in

    Args:
        f (Callable): Function to decorate

    Returns:
        Callable: Decorated function
    '''
    @wraps(f)
    def wrapper(request: HttpRequest, *args, **kwargs) -> Callable:
        return f(request, *args, **kwargs) if request.user.is_authenticated else redirect('/login')
    return wrapper
