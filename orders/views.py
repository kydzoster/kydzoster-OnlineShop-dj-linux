from django.urls import reverse
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

# This will create a views generated by order objects from forms.py.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        # validates data sent in the request
        form = OrderCreateForm(request.POST)
        # if valid ..
        if form.is_valid():
            # .. create a new order in db
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            # clear the cart when completed
            cart.clear()
            # launch asynchronos task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

# check is_active and is_staff fields of the user requesting the page are set to True
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

# This will generate PDF invoice for an order, only staff users can access this view
@staff_member_required
def admin_order_pdf(request, order_id):
    # get order object by ID ..
    order = get_object_or_404(Order, id=order_id)
    # .. then rendered HTML is saved in html variable
    html = render_to_string('orders/order/pdf.html', {'order': order})
    # then generate new httpresponse object by specifying it
    response = HttpResponse(content_type='application/pdf')
    # then include content disposition header to specify the filname
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    # use weasyprint to generate PDF firle from the rendered HTML and then write to httpresponse object
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(
        # use static file pdf.css to add css styling for the PDF file
        settings.STATIC_ROOT + 'css/pdf.css')])
    # return generated response
    return response