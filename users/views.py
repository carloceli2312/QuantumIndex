# QuantumIndex/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View, RedirectView
from django.urls import reverse_lazy
from django.db import IntegrityError
from quantumBlog.models import Post


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Le password non coincidono")
            return render(request, self.template_name)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, f"Account creato con successo! Benvenuto, {user.username}!")
            return redirect('index')
        except IntegrityError:
            messages.error(request, "Username o email già in uso. Per favore, scegline un altro.")
        except Exception as e:
            messages.error(request, f"Si è verificato un errore durante la registrazione: {str(e)}")

        return render(request, self.template_name)


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        login_identifier = request.POST.get('login_identifier')
        password = request.POST.get('password')
        
        if '@' in login_identifier:
            # È un'email, cerchiamo l'utente corrispondente
            try:
                user = User.objects.get(email=login_identifier)
                username = user.username
            except User.DoesNotExist:
                messages.error(request, "Nessun utente trovato con questa email.")
                return render(request, self.template_name)
        else:
            # È uno username
            username = login_identifier
        
        # Tentiamo l'autenticazione
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Benvenuto, {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Credenziali non valide. Per favore riprova.")
        
        return render(request, self.template_name)


class LogoutView(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return super().get(request, *args, **kwargs)


class ProfileView(View):
    template_name = 'profile.html'
    context = {
        'posts': Post.objects.all()
    }

    def get(self, request):
        return render(request, self.template_name, self.context)
