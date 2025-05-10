from django.shortcuts import render
from django.http import JsonResponse
from temphumidity.models import TempHumidityReading

def temphumidity_data(request):
    
    num_records = request.GET.get('num_records', 100)
    
    latest_data = TempHumidityReading.objects.order_by('-timestamp').all()[:num_records]
    
    data = [
        {
            'timestamp': record.timestamp,
            'temperature': record.temperature,
            'humidity': record.humidity
        }
        for record in latest_data
    ]
    
    return JsonResponse(data, safe=False)
