from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
from ..forms.SignUpForm import SignUpForm
from ..models import CustomUser, Statistic

def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated: return HttpResponseRedirect('/')

    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
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

            return HttpResponseRedirect('/login')
        
        else:
            if form.errors.get('username'): return HttpResponseBadRequest('<p class="error">Ce nom d\'utilisateur est déjà pris.</p>')
            if form.errors.get('email'): return HttpResponseBadRequest('<p class="error">Cette adresse email est déjà utilisée.</p>')
            if form.errors.get('password2'): return HttpResponseBadRequest('<p class="error">Le mot de passe est trop commun.</p>')

    return HttpResponseBadRequest()
