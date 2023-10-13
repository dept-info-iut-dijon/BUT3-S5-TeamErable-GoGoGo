from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from ..forms.ResetPasswordForm import ResetPasswordForm
from django.contrib.auth import authenticate, login, logout

def password_reset_confirm(request: HttpRequest, uidb64, token) -> HttpResponse:
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk=user_id)

        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                # Assuming the form is valid, update the user's password
                password = form.cleaned_data['password1']
                user.set_password(password)
                user.save()

                # Log the user in (optional)
                login(request, user)

                return render(request, 'profil.html')

        if default_token_generator.check_token(user, token):
            return render(request, 'password_reset_form.html', {'form':ResetPasswordForm(),'user':user, 'token':token})
        else:
            return render(request, 'password_reset_token_invalid.html')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'password_reset_token_invalid.html')