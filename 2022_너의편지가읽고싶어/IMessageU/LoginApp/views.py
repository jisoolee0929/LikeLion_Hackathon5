from django.shortcuts import render, redirect
from django.contrib import auth
from .models import User, UserManager
#from django.contrib.auth.models import User

# Create your views here.
def signup(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    found_user = User.objects.filter(email=email)
    if len(found_user):
      error = "이미 똑같은 아이디가 존재합니다."
      return render(request, 'signup.html', {'error':error})
    new_user = User.objects.create_user(email=email, password=password)
    auth.login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('home')
  return render(request, 'signup.html')

def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    user = auth.authenticate(request, email=email, password=password)
    if user is not None:
      auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      #auth.login(request, user)

      #return redirect('home')
      return redirect(request.GET.get('next', '/'))
    error = "아이디 또는 비밀번호가 틀립니다."
    return render(request, 'login.html', {'error': error})
  return render(request, 'login.html')

def logout(request):
  auth.logout(request)
  
  return redirect('home')