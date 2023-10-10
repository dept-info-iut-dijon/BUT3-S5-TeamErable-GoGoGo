from django.http import FileResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponse

def header_pfp(request: HttpRequest) -> FileResponse:
    if not request.user.is_authenticated: return HttpResponseForbidden()

    if request.user.profile_picture:
        return FileResponse(request.user.profile_picture)

    return HttpResponseNotFound()

def header_profile_name(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return ''

    return HttpResponse(f'{request.user.username}<br/><span>Utilisateur</span>')
