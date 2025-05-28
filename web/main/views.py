from django.shortcuts import render
from .func import geo, meteo
from django.http import JsonResponse, HttpRequest
from .models import City
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import CharField
from django.db.models.functions import Lower

CharField.register_lookup(Lower)

def index(request):   
    history = request.session.get('history', [])
    return render(request, 'main/index.html', {'history': history})

def get_cities(request):

    query = request.GET.get('query', '').strip()
    if query == '':
        return JsonResponse({'status': 'error', 'message': 'Empty query.'})
    
    cities = City.objects.filter(name__istartswith=query).order_by('name').values_list('name', flat=True)[:5]
    return JsonResponse({'status': 'success', 'cities': tuple(cities)})

def get_weather(request: HttpRequest):
    
    query = request.GET.get('query', '').strip()
    
    if query == '':
        return JsonResponse({'status': 'error', 'message': 'Empty query.'})
    
    cities = City.objects.filter(name__lower=query.lower())
    if cities.exists():
        c = cities.first()
        c.counter += 1
        c.save()
    else:
        t = TrigramSimilarity('name', query)
        cities = City.objects.annotate(similarity=t).filter(similarity__gt=0.2).order_by('-similarity')[:1]
        if cities.exists():
            с = cities.first()
            c.counter += 1
            c.save()

    
    history = request.session.get('history', [])
            
    if query in history:
        history.remove(query)
    history.insert(0, query)
    
    request.session['history'] = history[:5]
    request.session.modified = True
    
    lat, log = geo(query)
    if not lat or not log:
        return JsonResponse({'status': 'error', 'message': 'Can\'t find place.'})

    data = meteo(lat, log)

    return JsonResponse({'status': 'success', 'data': data, 'history': history}, safe=False)


def get_stats(request: HttpRequest):

    cities = City.objects.filter(counter__gt=0)
    data = {}
    for c in cities:
        data[c.name] = c.counter

    return JsonResponse(data)