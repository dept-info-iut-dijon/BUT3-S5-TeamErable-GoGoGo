from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..forms.SignUpForm import SignUpForm

def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated: return HttpResponseRedirect('/')

    if request.method == 'GET':
        form = SignUpForm(request.POST)
        return render(request, 'signup.html', {'form':form})
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # TODO: Implement registration
        if form.is_valid():
            user = form.save()
        return HttpResponseRedirect('/register')
