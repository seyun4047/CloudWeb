from django.shortcuts import render

# Create your views here.
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserForm
from . import _ads

def Ads(request):
    r = _ads.Ads(request)
    return r
def logout_view(request):
    logout(request)
    return redirect('/')

def mainpage(request):
    return render(request, 'common/main.html')

def contactpage(request):
    return render(request, 'common/contactpage.html')
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})