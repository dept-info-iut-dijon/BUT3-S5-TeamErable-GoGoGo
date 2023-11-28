from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render
from ....forms.ResetPasswordForm import ResetPasswordForm
from django.contrib.auth import login
from ...decorators import logout_required, request_type, RequestType

@logout_required
@request_type(RequestType.POST)
def password_reset_confirm(request: HttpRequest, uidb64: bytes | str, token: bytes | str) -> HttpResponse:
    '''Controlleur de la page de confirmation de réinitialisation de mot de passe

    Args:
        request (HttpRequest): La requête HTTP
        uidb64 (_type_): ID de l'utilisateur
        token (_type_): Token de réinitialisation de mot de passe

    Returns:
        HttpResponse: La réponse HTTP à la requête de confirmation de réinitialisation de mot de passe
    '''
    ret: HttpResponse = HttpResponseBadRequest()

    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk = user_id)

        if request.method == RequestType.POST.value:
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                # Assuming the form is valid, update the user's password
                password = form.cleaned_data['password1']
                user.set_password(password)
                user.save()

                # Log the user in (optional)
                login(request, user)

                ret = render(request, 'profile/profil.html')

        elif default_token_generator.check_token(user, token):
            ret = render(request, 'connection/password_reset_form.html', {'form':ResetPasswordForm(),'user':user, 'token':token})
        else:
            ret = render(request, 'connection/password_reset_token_invalid.html')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        ret = render(request, 'connection/password_reset_token_invalid.html')

    return ret
