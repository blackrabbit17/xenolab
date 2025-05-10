from django.http import JsonResponse
from django.http import HttpResponse
import json
import os


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