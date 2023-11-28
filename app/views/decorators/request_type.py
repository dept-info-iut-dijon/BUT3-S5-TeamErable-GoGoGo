from django.http import HttpRequest, HttpResponseBadRequest
from functools import wraps
from typing import Callable
from enum import StrEnum

class RequestType(StrEnum):
    '''Enum of request types'''

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'
    CONNECT = 'CONNECT'


def request_type(*request_types: RequestType) -> Callable:
    '''Decorator to restrict the request type

    Args:
        request_types (RequestType): Request types (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, TRACE, CONNECT)

    Returns:
        Callable: Decorated function
    '''

    rtypes = [rt.value for rt in request_types]

    def decorator(f: Callable) -> Callable:
        def wrapper(request: HttpRequest, *args, **kwargs) -> Callable:
            return f(request, *args, **kwargs) if request.method in rtypes else HttpResponseBadRequest()
        return wrapper
    return decorator
