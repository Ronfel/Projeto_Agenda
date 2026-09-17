from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from contact.forms import RegisterForm, RegisterUpdateForm



def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário Registrado')
            return redirect('login')

    return render(
        request,
        'contact/register.html',
        {
            'form': form,
            'site_title': 'Create User - ',
        }
    )

def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Usuário Logado')
            return redirect('index')
    
    return render(
        request,
        'contact/login.html',
        {
            'form': form,
            'site_title': 'Login - ',
        }
    ) 

def logout_view(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method == 'POST':
        form = RegisterUpdateForm(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário Atualizado')
            return redirect('index')

    return render(
        request,
        'contact/register.html',
        {
            'form': form,
            'site_title': 'Update User - ',
        }
    )
