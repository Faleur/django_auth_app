from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import datetime
from .models import SensorData
from django.http import JsonResponse
from .serializers import SensorDataSerializer  # Assurez-vous que cet import est correct

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='Optionnel mais recommandé.')

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Erreur dans le champ {field}: {error}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'registration/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer les dernières données des capteurs
    try:
        latest_data = SensorData.get_latest()
    except SensorData.DoesNotExist:
        latest_data = None
    
    context = {
        'sensor_data': latest_data,
        'page': 'home'
    }
    return render(request, 'home.html', context)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer les dernières données des capteurs
    try:
        latest_data = SensorData.get_latest()
    except SensorData.DoesNotExist:
        latest_data = None
    
    # Récupérer l'historique des données (20 derniers points)
    historical_data = SensorData.objects.order_by('-timestamp')[:20]
    
    context = {
        'sensor_data': latest_data,
        'historical_data': historical_data,
        'page': 'dashboard'
    }
    return render(request, 'sensors_dashboard.html', context)

def temperature(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer les dernières données des capteurs
    try:
        latest_data = SensorData.get_latest()
    except SensorData.DoesNotExist:
        latest_data = None
    
    # Récupérer l'historique des données (20 derniers points)
    historical_data = SensorData.objects.exclude(temperature=None).order_by('-timestamp')[:20]
    
    context = {
        'sensor_data': latest_data,
        'historical_data': historical_data,
        'page': 'temperature'
    }
    return render(request, 'temperature.html', context)

def humidity(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer les dernières données des capteurs
    try:
        latest_data = SensorData.get_latest()
    except SensorData.DoesNotExist:
        latest_data = None
    
    # Récupérer l'historique des données (20 derniers points)
    historical_data = SensorData.objects.exclude(humidity=None).order_by('-timestamp')[:20]
    
    context = {
        'sensor_data': latest_data,
        'historical_data': historical_data,
        'page': 'humidity'
    }
    return render(request, 'humidity.html', context)

def temperature(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer les dernières données des capteurs
    try:
        latest_data = SensorData.get_latest()
    except SensorData.DoesNotExist:
        latest_data = None
    
    # Récupérer l'historique des données (20 derniers points)
    historical_data = SensorData.objects.exclude(temperature=None).order_by('-timestamp')[:20]
    
    context = {
        'sensor_data': latest_data,
        'historical_data': historical_data,
        'page': 'temperature'
    }
    return render(request, 'temperature.html', context)

def luminosity(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer les dernières données des capteurs
    try:
        latest_data = SensorData.get_latest()
    except SensorData.DoesNotExist:
        latest_data = None
    
    # Récupérer l'historique des données (20 derniers points)
    historical_data = SensorData.objects.exclude(luminosity=None).order_by('-timestamp')[:20]
    
    context = {
        'sensor_data': latest_data,
        'historical_data': historical_data,
        'page': 'luminosity'
    }
    return render(request, 'luminosity.html', context)

def history(request):
    return render(request, 'history.html')

def reports(request):
    return render(request, 'reports.html')

def sensors_dashboard(request):
    return render(request, 'sensors_dashboard.html')