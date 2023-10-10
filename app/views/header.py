from django.http import FileResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound

def header_pfp(request: HttpRequest) -> FileResponse:
    if not request.user.is_authenticated: return HttpResponseForbidden()

    if request.user.profile_picture:
        return FileResponse(request.user.profile_picture)

    return HttpResponseNotFound()
