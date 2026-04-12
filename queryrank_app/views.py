import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from services.gpt_service import YandexGPTService

from django.conf import settings

from .forms import AddProductForm, ContactForm, SearchForm, UploadFileForm
from .models import Category, Product, Tag

menu = [
    {'title': 'Главная', 'url_name': 'index'},
    {'title': 'О системе', 'url_name': 'system'},
    {'title': 'Контакты', 'url_name': 'contact'},
]

def index(request):
    """Главная страница со списком товаров"""
    products = Product.published.all()[:12]
    context = {
        'title': 'QueryRank - Поиск товаров с ИИ',
        'menu': menu,
        'products': products,
    }
    return render(request, 'index.html', context)

def show_category(request, cat_slug):
    """Товары по категории"""
    category = get_object_or_404(Category, slug=cat_slug)
    products = Product.published.filter(cat=category)
    context = {
        'title': f'Категория: {category.name}',
        'menu': menu,
        'products': products,
        'cat_selected': category.pk,
    }
    return render(request, 'index.html', context)

def show_tag_products(request, tag_slug):
    """Товары по тегу"""
    tag = get_object_or_404(Tag, slug=tag_slug)
    products = tag.products.filter(status=Product.Status.PUBLISHED)
    context = {
        'title': f'Тег: {tag.name}',
        'menu': menu,
        'products': products,
        'cat_selected': 0,
    }
    return render(request, 'index.html', context)

def product_detail(request, product_slug):
    """Страница отдельного товара"""
    product = get_object_or_404(Product, slug=product_slug, status=Product.Status.PUBLISHED)
    context = {
        'title': product.title,
        'menu': menu,
        'product': product,
    }
    return render(request, 'product_detail.html', context)

def search_results(request):
    form = SearchForm(request.GET)
    products = Product.published.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        category = form.cleaned_data.get('category')
        
        if query:
            products = products.filter(title__icontains=query)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if category:
            products = products.filter(cat=category)
    
    context = {
        'title': 'Результаты поиска',
        'products': products,
        'form': form,
    }
    return render(request, 'search_results.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.status = Product.Status.PUBLISHED
            product.save()
            form.save_m2m()  # Сохранение связей many-to-many
            messages.success(request, f'Товар "{product.title}" успешно добавлен!')
            return redirect('product', product_slug=product.slug)
    else:
        form = AddProductForm()
    
    context = {
        'title': 'Добавление товара',
        'form': form,
    }
    return render(request, 'add_product.html', context)

def upload_image(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохранение файла через модель
            from .models import UploadedImage
            uploaded = UploadedImage(image=form.cleaned_data['file'])
            uploaded.save()
            messages.success(request, 'Изображение успешно загружено!')
            return redirect('upload_image')
    else:
        form = UploadFileForm()
    
    context = {
        'title': 'Загрузка изображения',
        'form': form,
    }
    return render(request, 'upload_image.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Здесь можно отправить письмо или сохранить в БД
            messages.success(request, 'Сообщение отправлено! Мы свяжемся с вами.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'title': 'Обратная связь',
        'form': form,
    }
    return render(request, 'contact.html', context)

def category_products(request, category_slug):
    """Товары по категориям"""
    products = Product.published.filter(category=category_slug)
    context = {
        'title': f'Товары категории: {category_slug}',
        'menu': menu,
        'products': products,
    }
    return render(request, 'queryrank/category.html', context)

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

def map_view(request):
    """Страница с картой"""
    context = {
        'title': 'Карта проезда',
        'api_key': settings.YANDEX_MAPS_API_KEY,
    }
    return render(request, 'map.html', context)

def ai_assistant(request):
    """Страница AI-ассистента"""
    return render(request, 'ai_assistant.html', {'title': 'AI-ассистент QueryRank'})

@csrf_exempt
def ai_chat_api(request):
    """API для обработки запросов к YandexGPT"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
            
            if not question:
                return JsonResponse({'error': 'Введите вопрос'}, status=400)
            
            gpt_service = YandexGPTService()
            answer = gpt_service.answer_question(question)
            
            return JsonResponse({'answer': answer})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Неверный формат запроса'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

@csrf_exempt
def generate_description_api(request):
    """API для генерации описания товара"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_name = data.get('product_name', '')
            features = data.get('features', '')
            
            if not product_name:
                return JsonResponse({'error': 'Укажите название товара'}, status=400)
            
            gpt_service = YandexGPTService()
            description = gpt_service.generate_product_description(product_name, features)
            
            return JsonResponse({'description': description})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)