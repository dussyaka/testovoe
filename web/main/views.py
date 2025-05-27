from django.shortcuts import render
from .func import geo, meteo
from django.http import JsonResponse


def index(request):
    return render(request, 'main/index.html')

def get_cities(request):
    pass

def get_weather(request):
    print(request.GET.dict())
    
    query = request.GET.get('query', '').strip()
    if query == '':
        return JsonResponse({'status': 'error', 'message': 'Empty query.'})
    
    lat, log = geo(query)
    if not lat or not log:
        return JsonResponse({'status': 'error', 'message': 'Can\'t find place.'})

    data = meteo(lat, log)

    return JsonResponse({'status': 'success', 'data': data}, safe=False)