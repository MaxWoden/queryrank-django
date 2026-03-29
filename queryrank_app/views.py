from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render

def index(request):
    return render(request, 'index.html')

def system(request):
    return render(request, 'system.html')

def contact(request):
    return render(request, 'contact.html')

def categories(request):
    return HttpResponse("<h1>Категории фильтрации</h1>")

def filter_detail(request, filter_id):
    return HttpResponse(f"<h1>Фильтр {filter_id}</h1>")

def route_info(request, route_slug):
    return HttpResponse(
        f"<h1>Маршрут: {route_slug}</h1><p>Информация о направлении</p>"
    )

def search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        
        results_count = 15 

        return HttpResponse(f"По запросу '{query}' найдено {results_count} товаров")
    
    return HttpResponse("Форма поиска товаров")

def analyze_product(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_url = request.POST.get('product_url')
        return HttpResponse("Анализ товара выполнен успешно")
    return HttpResponse("Форма анализа товара")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def archive(request, year):
    if year > 2025:
        raise Http404("Архив за этот год еще не доступен")
    return HttpResponse(f"<h1>Архив за {year} год</h1>")

def old_page(request):
    return redirect('index')

def temp_redirect(request):
    return redirect('index', permanent=True)
