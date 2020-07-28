from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    # this will call product list without any parameter
    path('', views.product_list, name='product_list'),
    # this will filter products according to a given category
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    # this will pass id and slug parameters to retrieve a specific product
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
