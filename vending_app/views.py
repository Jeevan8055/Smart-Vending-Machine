from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal
from django.utils.timezone import now
from .models import Product, Transaction

def display_products(request):
    """ View to display the list of products """
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def process_transaction(request, product_id):
    """ View to process the transaction """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        amount_paid = Decimal(request.POST.get('amount_paid', product.price * quantity))

        # Check stock availability
        if quantity > product.stock:
            return render(request, 'transaction.html', {'product': product, 'error': "Not enough stock available!"})

        # Calculate change
        total_cost = product.price * quantity
        change = max(amount_paid - total_cost, 0)

        # Update stock
        product.stock -= quantity
        product.save()

        # Save transaction
        transaction = Transaction.objects.create(
            product=product,
            quantity=quantity,
            amount_paid=amount_paid,
            change=change,
            timestamp=now()
        )

        return redirect('transaction_success', transaction_id=transaction.id)

    return render(request, 'transaction.html', {'product': product})



def transaction_success(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    formatted_datetime = transaction.timestamp.strftime("%d-%m-%Y %I:%M %p")  # DD-MM-YYYY HH:MM AM/PM

    context = {
        'product': transaction.product,
        'quantity': transaction.quantity,
        'amount_paid': transaction.amount_paid,
        'change': transaction.change,
        'transaction_datetime': formatted_datetime,  # Updated variable
    }

    return render(request, 'transaction_result.html', context)



def api_validate_transaction(request):
    """ API endpoint to validate transaction """
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
            amount_paid = Decimal(request.POST.get('amount_paid', 0))
            
            product = get_object_or_404(Product, id=product_id)
            total_price = product.price * quantity

            if quantity > product.stock:
                return JsonResponse({'success': False, 'error': 'Not enough stock available.'})

            if amount_paid < total_price:
                return JsonResponse({'success': False, 'error': 'Insufficient funds.'})

            return JsonResponse({'success': True, 'message': 'Transaction valid.'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
