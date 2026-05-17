from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.username}!')
            next_url = request.GET.get('next', 'post_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Utilizador ou palavra-passe incorretos.')
    else:
        form = LoginForm(request)
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Sessão terminada.')
    return redirect('login')
