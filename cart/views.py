from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# this adds products to the cart or updates quantities for existing products
@require_POST # only POST requests
def cart_add(request, product_id):
    cart = Cart(request)
    # retrieve by ID
    product = get_object_or_404(Product, id=product_id)
    # validate form
    form = CartAddProductForm(request.POST)
    # if it's valid ..
    if form.is_valid():
        # .. add product
        cd = form.cleaned_data
        # .. update product
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

# removes items from the cart
@require_POST
# retrieves by product ID and removes from the cart
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

# gets the current cart to display it
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        # allows to change product quantity from the cart
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'cart/detail.html', {'cart': cart})