def cart_context(request):
    """Add cart information to all templates"""
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    cart_total = sum(item['price'] * item['quantity'] for item in cart.values())
    
    return {
        'cart_items': cart,
        'cart_count': cart_count,
        'cart_total': cart_total,
    }
