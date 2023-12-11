from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
from ...forms.SignUpForm import SignUpForm
from ...models import CustomUser, Statistic
from ..decorators import logout_required, request_type, RequestType
from ...http import HttpResponseNotifError

def _create_user(form: SignUpForm) -> CustomUser:
    '''Fonction qui cree un utilisateur a partir du formulaire
    Args:
        form (SignUpForm): Le formulaire de creation de compte
    
    Returns:
        CustomUser: L'utilisateur cree
    '''
    statistic = Statistic.objects.create(
        game_win = 0,
        game_loose = 0,
        game_ranked_win = 0,
        game_ranked_loose = 0,
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
    return user


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
        ret = render(request, 'connection/register.html')

    elif request.method == RequestType.POST.value:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = _create_user(form)
            ret = HttpResponseRedirect('/login')
        
        else:
            if form.errors.get('username'): ret = HttpResponseNotifError('Ce nom d\'utilisateur est déjà pris.')
            elif form.errors.get('email'): ret = HttpResponseNotifError('Cette adresse email est déjà utilisée.')
            elif form.errors.get('password2'): ret = HttpResponseNotifError('Le mot de passe est trop commun.')

    return ret
