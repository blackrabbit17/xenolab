from django.http import JsonResponse

import json
import os


from django.conf import settings


def get_lifeform_data(request):
    
    lifeform_dir = settings.BASE_DIR / 'assets' / 'lifeform.json'
    lifeform_data = json.load(open(lifeform_dir, 'r'))
    
    return JsonResponse(lifeform_data, safe=False)
