from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

# Task to send an e-mail notification when an order is successfully created.
@task
# define payment completed by using @task decorator
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)

    # use EmailMessage class to create an email object
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
    # generate PDF from rendered html template variable
    html = render_to_string('orders/order/pdf.html', {'order': order})
    # and output in BytesIO instance which is an in-memory bytes buffer
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach PDF file to the EmailMessage object using the attach(), including contents of out buffer
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    # send e-mail
    email.send()