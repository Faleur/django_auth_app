from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import SensorData
from django.utils import timezone

@csrf_exempt
@require_http_methods(["POST"])
def sensor_data(request):
    try:
        data = json.loads(request.body)
        sensor_data = SensorData.objects.create(
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            luminosity=data.get('luminosity'),
            timestamp=timezone.now(),
            is_connected=True
        )
        return JsonResponse({
            'status': 'success',
            'message': 'Data received successfully',
            'data': {
                'id': sensor_data.id,
                'timestamp': sensor_data.timestamp.isoformat()
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
