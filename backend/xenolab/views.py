from django.http import JsonResponse, HttpResponse
from django.conf import settings
import json
from sunlight.models import Sunlight
from wind.models import Wind


def get_lifeform_data(request):
    lifeform_type = request.GET.get('type', 'venus')  # Default to venus fly trap
    
    # Choose the correct lifeform JSON file based on type
    if lifeform_type == 'venus':
        lifeform_file = 'lifeform.venus.json'
    elif lifeform_type == 'pitcher':
        lifeform_file = 'lifeform.pitcher.json'
    elif lifeform_type == 'sundew':
        lifeform_file = 'lifeform.sundew.json'
    else:
        lifeform_file = 'lifeform.venus.json'  # Default
    
    lifeform_path = settings.BASE_DIR / 'assets' / lifeform_file
    with open(lifeform_path, 'r') as file:
        lifeform_data = json.load(file)
    
    return JsonResponse(lifeform_data, safe=False)


def map_png(request):
    lifeform_type = request.GET.get('type', 'venus')  # Default to venus fly trap
    
    # Choose the correct lifeform JSON file based on type
    if lifeform_type == 'venus':
        map_file = 'venus_fly_trap.png'
    elif lifeform_type == 'pitcher':
        map_file = 'pitcher.png'
    elif lifeform_type == 'sundew':
        map_file = 'sundew.png'
    else:
        map_file = 'venus_fly_trap.png'  # Default
    
    map_path = settings.BASE_DIR / 'assets' / map_file
    try:
        with open(map_path, 'rb') as file:
            map_data = file.read()
        return HttpResponse(map_data, content_type='image/png')
    except FileNotFoundError:
        return HttpResponse(status=404)


def get_atmospherics(request):
    sunlight_data = Sunlight.objects.all().order_by('-timestamp')[:1]
    wind_data = Wind.objects.all().order_by('-timestamp')[:1]

    # Create default values in case no records exist yet
    sunlight = {
        'status': 0,
        'r': 0.0,
        'g': 0.0,
        'b': 0.0,
        'brightness': 0.0,
    }
    
    wind = {
        'status': 0,
        'speed': 0.0,
    }
    
    # If we have actual records, use those values
    if sunlight_data.exists():
        s = sunlight_data[0]
        sunlight = {
            'status': s.status,
            'r': s.r,
            'g': s.g,
            'b': s.b,
            'brightness': s.brightness,
        }
    
    if wind_data.exists():
        w = wind_data[0]
        wind = {
            'status': w.status,
            'speed': w.speed,
        }
    
    payload = {
        'sunlight': sunlight,
        'wind': wind,
    }
    
    return JsonResponse(payload)
