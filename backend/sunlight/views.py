from django.http import JsonResponse
from sunlight.models import Sunlight


def sunlight_data(request):

    num_records = request.GET.get('num_records', 100)
    
    latest_data = Sunlight.objects.order_by('-timestamp').all()[:num_records]
    
    data = [
        {
            'timestamp': record.timestamp,
            'r': record.r,
            'g': record.g,
            'b': record.b,
            'brightness': record.brightness,
            'status': record.status
        }
        for record in latest_data
    ]
    
    return JsonResponse(data, safe=False)

