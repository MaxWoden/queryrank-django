from django.db import models
from django.urls import reverse

class PublishedManager(models.Manager):
    """Менеджер для получения только опубликованных товаров"""
    def get_queryset(self):
        return super().get_queryset().filter(status=Product.Status.PUBLISHED)

class Product(models.Model):
    """Модель товара для интернет-магазина"""
    
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    
    class CategoryType(models.TextChoices):
        ELECTRONICS = 'electronics', 'Электроника'
        CLOTHING = 'clothing', 'Одежда'
        HOME = 'home', 'Дом и сад'
        BOOKS = 'books', 'Книги'
        TOYS = 'toys', 'Игрушки'
        SPORTS = 'sports', 'Спорт и отдых'
    
    # Основные поля
    title = models.CharField(max_length=255, verbose_name="Название товара")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    category = models.CharField(max_length=50, choices=CategoryType.choices, 
                                default=CategoryType.ELECTRONICS, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")
    brand = models.CharField(max_length=100, blank=True, verbose_name="Бренд")
    rating = models.FloatField(default=0, verbose_name="Рейтинг")
    status = models.BooleanField(choices=Status.choices, default=Status.DRAFT, 
                                  verbose_name="Статус")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, 
                            verbose_name="Категория", related_name='products')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name="Теги", 
                                   related_name='products')
    
    photo = models.ImageField(
        upload_to="products/photos/%Y/%m/%d/",
        blank=True, 
        null=True, 
        verbose_name="Изображение товара"
    )
    
    # Менеджеры
    objects = models.Manager()  # Стандартный менеджер
    published = PublishedManager()  # Менеджер для опубликованных товаров
    
    class Meta:
        ordering = ['-time_create']  # Сортировка по времени создания (новые сверху)
        indexes = [
            models.Index(fields=['-time_create']),
            models.Index(fields=['category']),
            models.Index(fields=['price']),
        ]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def get_absolute_url(self):
        """Возвращает URL для просмотра товара"""
        return reverse('product', kwargs={'product_slug': self.slug})

    def get_details(self):
        """Возвращает связанный объект ProductDetails (если есть)"""
        return getattr(self, 'details', None)
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    """Модель категорий товаров"""
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    """Модель тегов для товаров"""
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название тега")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    
    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})
    
    def __str__(self):
        return self.name
    
class ProductDetails(models.Model):
    """Дополнительные характеристики товара (связь один к одному с Product)"""
    product = models.OneToOneField(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='details',
        verbose_name="Товар"
    )
    weight = models.FloatField(default=0, verbose_name="Вес (кг)")
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="Размеры (ДхШхВ)")
    color = models.CharField(max_length=50, blank=True, verbose_name="Цвет")
    warranty_months = models.IntegerField(default=12, verbose_name="Гарантия (мес)")
    country_of_origin = models.CharField(max_length=100, blank=True, verbose_name="Страна производства")
    
    class Meta:
        verbose_name = "Детальная характеристика"
        verbose_name_plural = "Детальные характеристики"
    
    def __str__(self):
        return f"Характеристики {self.product.title}"
    
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name="Изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    
    class Meta:
        verbose_name = "Загруженное изображение"
        verbose_name_plural = "Загруженные изображения"
    
    def __str__(self):
        return f"Изображение от {self.uploaded_at}"