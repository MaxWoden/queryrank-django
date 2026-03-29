from django.urls import path
from . import views

handler404 = 'queryrank_app.views.page_not_found'

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/", views.categories, name="categories"),
    path('filter/<int:filter_id>/', views.filter_detail, name='filter_detail'),
    path('route/<slug:route_slug>/', views.route_info, name='route_info'),
    path("search/", views.search, name="search"),
    path("analyze/", views.analyze_product, name="analyze"),
    path("archive/<int:year>/", views.archive, name="archive"),
    path("old_page/", views.old_page, name="old_page"),
    path("temp_redirect/", views.temp_redirect, name="temp_redirect"),
    path('system/', views.system, name='system'),
    path('contact/', views.contact, name='contact'),
]