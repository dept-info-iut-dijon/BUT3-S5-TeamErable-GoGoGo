from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from ..forms.ForgottenPassForm import ForgottenPassForm
from ..models.person import CustomUser
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings


def send_password_reset_email(user, token):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    subject = "Recuperation de votre mot de passe"
    message = f"Bonjour, {user.username}!\n\n"
    message += "Vous avez fait une demande de recuperation de mot de passe. Pour reinitialiser votre mot de passe, cliquez sur le lien ci dessous:\n\n"
    # Generate a URL for the password reset confirmation view
    reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
    reset_url = "http://localhost:8080" + reset_url  # Adjust the protocol and domain as needed in production

    message += reset_url + "\n\n"
    message += "Si vous n'etes pas a l'origine de cette demande, ignorez cet email.\n\n"
    message += "L'equipe Go-Go-Go"
    # Send the email
    from_email = settings.DEFAULT_FROM_EMAIL  # Use the default from_email from settings
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    

def forgotten_password(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ForgottenPassForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                print("try")
                #On verifie si le un utilisateur a cette email
                user = CustomUser.objects.get(email=email)
                print("found")
                # Geneneration d'un token
                token = default_token_generator.make_token(user)
                print("token")
                # Envoie du mail 
                send_password_reset_email(user, token)
                # Redirect to a "Password Reset Requested" page
                print("sent")
                return render(request, 'password_reset_request_success.html')
            except CustomUser.DoesNotExist:
                # Handle the case where the email is not found
                pass
    else:
        form = ForgottenPassForm()
    return render(request, 'forgottenpassword.html', {'form':form})
