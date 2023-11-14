from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
from ..forms.SignUpForm import SignUpForm
from ..models import CustomUser, Statistic
from .decorators import logout_required, request_type, RequestType

@logout_required
@request_type(RequestType.GET, RequestType.POST)
def register(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page d'inscription

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête d'inscription
    '''

    ret: HttpResponse = HttpResponseBadRequest()

    if request.method == RequestType.GET.value:
        ret = render(request, 'register.html')

    elif request.method == RequestType.POST.value:
        form = SignUpForm(request.POST)
        if form.is_valid():
            statistic = Statistic.objects.create(
                game_win = 0,
                game_loose = 0,
                game_ranked_win = 0,
                game_ranked_loose = 0,
                average_time_move = 0,
            )

            user = CustomUser.objects.create(
                username = form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = '',
                stat = statistic,
            )

            user.set_password(form.cleaned_data['password1'])

            with open('./static/icons/default-pfp.png', 'rb') as f:
                user.profile_picture.save('default-pfp.png', f, save=True)

            ret = HttpResponseRedirect('/login')
        
        else:
            if form.errors.get('username'): ret = HttpResponseBadRequest('<p class="error">Ce nom d\'utilisateur est déjà pris.</p>')
            elif form.errors.get('email'): ret = HttpResponseBadRequest('<p class="error">Cette adresse email est déjà utilisée.</p>')
            elif form.errors.get('password2'): ret = HttpResponseBadRequest('<p class="error">Le mot de passe est trop commun.</p>')

    return ret
