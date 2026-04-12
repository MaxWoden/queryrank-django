from django.contrib import admin, messages
from .models import Product, Category, ProductDetails, Tag, UploadedImage
from django.utils.safestring import mark_safe

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category', 'status', 'time_create', 'rating', 'get_image')
    list_display_links = ('id', 'title')
    list_editable = ('price', 'status')
    ordering = ('-time_create', 'title')
    list_per_page = 10
    search_fields = ('title', 'description', 'brand', 'cat__name')
    list_filter = ('cat', 'status', 'tags', 'category')

    fields = ['title', 'slug', 'cat', 'category', 'price', 'brand', 
              'rating', 'description', 'tags', 'status']
    readonly_fields = ['time_create', 'time_update']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']

    @admin.display(description="Изображение")
    def get_image(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" style="object-fit: cover;">')
        return "Без фото"

    @admin.display(description="Краткое описание")
    def brief_info(self, product: Product):
        desc_len = len(product.description) if product.description else 0
        return f"Описание: {desc_len} симв., Бренд: {product.brand or '—'}"

    actions = ['make_published', 'make_draft']
    
    @admin.action(description="Опубликовать выбранные товары")
    def make_published(self, request, queryset):
        count = queryset.update(status=Product.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} товаров(а)", messages.SUCCESS)
    
    @admin.action(description="Снять с публикации выбранные товары")
    def make_draft(self, request, queryset):
        count = queryset.update(status=Product.Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} товаров(а)", messages.WARNING)

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_image', 'uploaded_at')
    list_display_links = ('id', 'get_image')
    readonly_fields = ('get_image',)
    
    @admin.display(description="Изображение")
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" style="object-fit: cover;">')
        return "Без фото"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductDetails)
class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'weight', 'warranty_months', 'country_of_origin')
    list_display_links = ('id', 'product')
    list_editable = ('weight', 'warranty_months')
    search_fields = ('product__title', 'country_of_origin')