from .header import header_pfp, header_profile_name, get_pfp
from django.http import FileResponse

def favicon(request):
    return FileResponse(open('static/icons/favicon.svg', 'rb'))
