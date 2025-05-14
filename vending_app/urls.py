from django.urls import path
from .views import display_products, process_transaction, transaction_success, api_validate_transaction

urlpatterns = [
    path('', display_products, name='display_products'),
    path('buy/<int:product_id>/', process_transaction, name='process_transaction'),
    path('transaction_success/<int:transaction_id>/', transaction_success, name='transaction_success'),
    path('api/validate/', api_validate_transaction, name='api_validate_transaction'),
]
