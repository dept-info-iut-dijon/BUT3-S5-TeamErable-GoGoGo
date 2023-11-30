from django.http import HttpRequest

def verify_post(request: HttpRequest, key : str, message : str) -> str:
    if (value := request.POST.get(key)) is None: 
        raise Exception(message)
    return value

def verify_get(request: HttpRequest, key : str, message : str) -> str:
    if (value := request.GET.get(key)) is None: 
        raise Exception(message)
    return value
