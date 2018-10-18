from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from dashboard.models import Project
from .forms import PaymentForm, OrderForm
from .models import Order, OrderLineItem
from dashboard.models import Project
import stripe


stripe.api_key = settings.STRIPE_SECRET

@login_required()
def confirm(request, pk):
    """ Renders the payment confirmation page """
    project = get_object_or_404(Project, pk=pk)
    total = project.fee + project.plus_vat
    return render(request, 'confirm.html', {'project': project, 'total': total})

@login_required()
def confirm_payment(request, id):
    """ Adds project to user's cart and redirects to checkout """
    cart = request.session.get('cart', {})
    cart[id] = cart.get(id)
    request.session['cart'] = cart
    print(cart)
    return redirect(checkout)

@login_required()
def checkout(request):
    """ Renders the checkout/payment page for each project """
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = PaymentForm(request.POST)
        
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            
            cart = request.session.get('cart', {})
            total = 0
            for id in cart.items():
                project = get_object_or_404(Project, pk=id[0])
                total = project.fee + project.plus_vat
                order_line_item = OrderLineItem(
                    order = order,
                    project = project
                    )
                order_line_item.save()
                project.paid=True
                project.save()
            context = {
                'project': project,
                'total': total,
            }
            try:
                customer = stripe.Charge.create(
                    amount = int(total * 100),
                    currency = "GBP",
                    description = request.user.email,
                    card = payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Sorry. Your card has been declined. Please try again.")
            
            if customer.paid:
                request.session['cart'] = {}
                return redirect(receipt, project.pk)
            else:
                messages.error(request, "Sorry. We were unable to process your payment. Please try again.")
        else:
            print(payment_form.errors)
            messages.error(request, "Sorry. We were unable to take payment with that card.")
    else:
        payment_form = PaymentForm()
        order_form = OrderForm()
    context = {
        'order_form': order_form,
        'payment_form': payment_form,
        'publishable': settings.STRIPE_PUBLISHABLE,
    }
    return render(request, 'checkout.html', context)

@login_required()
def receipt(request, pk):
    """ Renders the receipt page """
    project = get_object_or_404(Project, pk=pk)
    total = project.fee + project.plus_vat
    return render(request, 'receipt.html', {'project': project, 'total': total})