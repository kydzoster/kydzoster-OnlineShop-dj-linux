from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

# this view will retrieve and list all the products by a given category
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    # This will retrieve only available products
    products = Product.objects.filter(available=True)
    # filtering process by a given category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
        })

# this view will retrieve and display a single product
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
        })
