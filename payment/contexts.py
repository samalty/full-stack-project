from django.shortcuts import get_object_or_404
from dashboard.models import Project

def cart_contents(request):
    """ Ensures cart contents is rendered within checkout page """
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    project_count = 0
    for id, quantity in cart.items():
        project = get_object_or_404(Project, pk=id)
        total += project.fee + project.plus_vat
        project_count += quantity
        cart_items.append({'id': id, 'quantity': quantity, 'project': project})
    return { 'cart_items': cart_items, 'total': total, 'project_count': project_count }