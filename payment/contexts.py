from django.shortcuts import get_object_or_404
from dashboard.models import Project

def cart_contents(request):
    """ Ensures cart contents is rendered within checkout page """
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for id in cart.items():
        project = get_object_or_404(Project, pk=id[0])
        total += project.fee + project.plus_vat
        cart_items.append({'id': id, 'project': project})
    return { 'cart_items': cart_items, 'total': total}