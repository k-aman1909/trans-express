from django.http import JsonResponse
from django.shortcuts import HttpResponse,render,redirect
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import logout
from PCPLapp import models
from django.utils.http import  urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import login
from django.utils.encoding import force_bytes,force_str
from django.contrib import messages, auth
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetView as BasePasswordResetView
from django import http
from django.contrib.auth import get_user_model 
User = get_user_model()
# Create your views here.


# logistics/views.py
from django.shortcuts import render, redirect
# from .forms import UserLoginForm, UserRegistrationForm

from .forms import CustomPasswordResetForm

class CustomPasswordResetView(BasePasswordResetView):
    form_class = CustomPasswordResetForm

def login(request):
    if request.method == 'POST':
        username=request.POST.get('name').strip()
        password=request.POST.get('pass').strip()
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login')
    else:
        return render(request, 'login.html')
def register(request):
    if request.method == 'POST':
        name = request.POST.get('username')    
        userid = request.POST.get('userid')    
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        try:
            if User.objects.filter(username=userid).exists():
                messages.error(request, 'Username is already taken.')
                return redirect('login')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
                return redirect('login')
            if User.objects.filter(phone_number=phone).exists():
                messages.error(request, 'Phone Number is already registered.')
                return redirect('login')
            User.objects.create(username=userid, first_name=name, email=email, phone_number=phone, is_active=False)
            user = User.objects.get(username=userid)
            user.set_password(password)
        
            user.save()
            
            messages.success(request, 'User created successfully. Please wait for admin approval')
            return redirect('login')
        except :
            messages.success(request, 'Data Matched')
            return redirect('login')
    else:
       
        return render(request, 'login.html')

def out(request):
    logout(request)
    return redirect('login')
def changepass(request):
    password=User.objects.values('password')    
    if request.method =='POST':
        
        oldpass=request.POST.get('oldpass').strip()
        newpass=request.POST.get('newpass').strip()
        user = auth.authenticate(request, username=request.user, password=oldpass)
        if user is not None:
            user = User.objects.get(username=request.user)
            user.set_password(newpass)
            user.save()
            messages.success(request, 'Password Successfully Changed')
            return redirect('login')
        else:
            messages.error(request, 'Invalid Password')
            return redirect('changepass')
            
    return render(request,'changepass.html')

def resetpass(request):
    return render(request,'resetpass.html')
def password_reset(request, uidb64, token):
    uid=force_str(urlsafe_base64_decode(uidb64)) 
    try:
        if request.method == "POST":
            newpassword1 = request.POST.get('newpass1').strip()
            newpassword2 = request.POST.get('newpass2').strip()
            if newpassword1 == newpassword2:   
                uid=force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=uid)
                user.set_password(newpassword1)
                user.save()
                messages.success(request, 'Password Change Successfully')
                return redirect('login')
            else:
                messages.info(request,'Password Does Not Match')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, 'resetpass.html')