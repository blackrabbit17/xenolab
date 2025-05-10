from django.http import JsonResponse
from wind.models import Wind


def wind_data(request):
    
    num_records = request.GET.get('num_records', 100)
    
    latest_data = Wind.objects.order_by('-timestamp').all()[:num_records]
    
    data = [
        {
            'timestamp': record.timestamp,
            'status': record.status
        }
        for record in latest_data
    ]
    
    return JsonResponse(data, safe=False)
