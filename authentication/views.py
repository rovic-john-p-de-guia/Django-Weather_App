from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('weather_index')  # Updated from 'index' to 'weather_index'
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'authentication/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('login')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('login')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('weather_index')  # Updated from 'index' to 'weather_index'
    
    return render(request, 'authentication/login.html')

# API Views
class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        return Response({
            "message": "This is a protected route",
            "user": request.user.username
        })

def custom_logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
