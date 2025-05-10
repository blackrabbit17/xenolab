from django.http import JsonResponse
from django.http import HttpResponse
import json
from sunlight.models import Sunlight
from wind.models import Wind


from django.conf import settings


def get_lifeform_data(request):
    
    lifeform_dir = settings.BASE_DIR / 'assets' / 'lifeform.json'
    lifeform_data = json.load(open(lifeform_dir, 'r'))
    
    return JsonResponse(lifeform_data, safe=False)


def map_png(request):
    
    lifeform_dir = settings.BASE_DIR / 'assets' / 'lifeform.json'
    lifeform_data = json.load(open(lifeform_dir, 'r'))
    
    map_dir = settings.BASE_DIR / 'assets' / lifeform_data['map']
    map_data = open(map_dir, 'rb').read()
    return HttpResponse(map_data, content_type='image/png')


def get_atmospherics(request):
    
    sunlight = Sunlight.objects.all().order_by('-timestamp')[:1]
    wind = Wind.objects.all().order_by('-timestamp')[:1]

    payload = {
        'sunlight': {
            'status': sunlight[0].status,   
            'r': sunlight[0].r,
            'g': sunlight[0].g,
            'b': sunlight[0].b,
            'brightness': sunlight[0].brightness,
        },
        'wind': {
            'status': wind[0].status,
            'speed': wind[0].speed,
        },
    }
    
    return JsonResponse(payload)
