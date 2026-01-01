from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import PendakiRegisterForm, AdminRegisterForm, UserLoginForm


def register_view(request):
    """View untuk memilih role saat registrasi"""
    return render(request, 'accounts/register_choice.html')


def register_pendaki_view(request):
    """View untuk registrasi Pendaki"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = PendakiRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, 
                f'Selamat datang, {user.get_full_name()}! Akun pendaki Anda berhasil dibuat.'
            )
            return redirect('core:home')
        else:
            messages.error(
                request, 
                'Terjadi kesalahan. Silakan periksa form kembali.'
            )
    else:
        form = PendakiRegisterForm()
    
    context = {
        'form': form,
        'page_title': 'Daftar sebagai Pendaki',
        'role': 'pendaki'
    }
    return render(request, 'accounts/register_form.html', context)


def register_admin_view(request):
    """View untuk registrasi Admin"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, 
                f'Selamat datang, {user.get_full_name()}! Akun admin Anda berhasil dibuat.'
            )
            return redirect('dashboard:admin')  # Redirect ke admin dashboard
        else:
            messages.error(
                request, 
                'Terjadi kesalahan. Silakan periksa form kembali.'
            )
    else:
        form = AdminRegisterForm()
    
    context = {
        'form': form,
        'page_title': 'Daftar sebagai Admin',
        'role': 'admin'
    }
    return render(request, 'accounts/register_form.html', context)


def login_view(request):
    """View untuk login (semua role)"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(username=email, password=password)
            
            if user is not None:
                login(request, user)
                
                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(1209600)
                
                messages.success(request, f'Selamat datang kembali, {user.get_full_name()}!')
                
                # Redirect berdasarkan role
                if user.is_admin_role:
                    return redirect('dashboard:admin')
                else:
                    next_page = request.GET.get('next', 'core:home')
                    return redirect(next_page)
        else:
            messages.error(request, 'Email atau password salah.')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'page_title': 'Login'
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout_view(request):
    """View untuk logout"""
    user_name = request.user.get_full_name()
    logout(request)
    messages.info(request, f'Anda telah logout. Sampai jumpa, {user_name}!')
    return redirect('core:home')


@login_required
def profile_view(request):
    """View untuk melihat profil user"""
    context = {
        'page_title': 'Profil Saya'
    }
    return render(request, 'accounts/profile.html', context)