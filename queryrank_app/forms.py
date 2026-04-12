from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from .models import Product, Category, Tag, ProductDetails

# Валидатор для проверки только русских символов
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    
    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел"
    
    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message)

# Форма для поиска товаров (не связанная с моделью)
class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100, 
        required=False,
        label="Поиск",
        widget=forms.TextInput(attrs={'class': 'search-input', 'placeholder': 'Введите название товара...'})
    )
    min_price = forms.DecimalField(
        required=False, 
        label="Цена от",
        widget=forms.NumberInput(attrs={'class': 'price-input', 'step': '100'})
    )
    max_price = forms.DecimalField(
        required=False, 
        label="Цена до",
        widget=forms.NumberInput(attrs={'class': 'price-input', 'step': '100'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False, 
        empty_label="Все категории",
        label="Категория"
    )

# Форма добавления товара (связанная с моделью)
class AddProductForm(forms.ModelForm):
    # Дополнительная настройка полей
    title = forms.CharField(
        max_length=255, 
        min_length=3,
        label="Название товара",
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        error_messages={
            'min_length': 'Название слишком короткое (минимум 3 символа)',
            'required': 'Название товара обязательно'
        }
    )
    
    class Meta:
        model = Product
        fields = ['title', 'slug', 'category', 'price', 'brand', 'description', 'status', 'cat', 'tags', 'photo']
        labels = {
            'slug': 'URL (slug)',
            'category': 'Тип категории',
            'price': 'Цена (₽)',
            'brand': 'Бренд',
            'description': 'Описание',
            'status': 'Статус публикации',
            'cat': 'Категория',
            'tags': 'Теги'
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-textarea'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'brand': forms.TextInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '100'}),
        }
    
    # Пользовательский валидатор для поля title
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Название товара не должно превышать 100 символов')
        return title
    
    # Пользовательский валидатор для поля slug
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Product.objects.filter(slug=slug).exists():
            raise ValidationError('Товар с таким URL уже существует')
        return slug

# Форма для загрузки файлов (не связанная с моделью)
class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Выберите изображение")

# Форма обратной связи (не связанная с моделью)
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше имя", widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    subject = forms.CharField(max_length=200, label="Тема", widget=forms.TextInput(attrs={'class': 'form-input'}))
    message = forms.CharField(label="Сообщение", widget=forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-textarea'}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email:
            raise ValidationError('Введите корректный email адрес')
        return email