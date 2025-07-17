from django.urls import path
from . import views
 
urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('create-transaction/', views.create_payment_transaction, name='create_transaction'),
] 