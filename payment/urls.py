from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    # processes payment
    path('process/', views.payment_process, name='process'),
    # redirect user if payment is successful
    path('done/', views.payment_done, name='done'),
    # redirect user if payment failed/canceled
    path('canceled/', views.payment_canceled, name='canceled'),
]