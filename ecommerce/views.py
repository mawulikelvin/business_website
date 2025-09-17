from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Product, Service, Category, Order, OrderItem, Customer, ContactMessage
import json
from datetime import datetime

def home(request):
    """Home page with featured products and services"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:4]
    featured_services = Service.objects.filter(is_featured=True, is_active=True)[:6]
    
    context = {
        'featured_products': featured_products,
        'featured_services': featured_services,
    }
    return render(request, 'ecommerce/home.html', context)

def products(request):
    """Product listing page with filtering and pagination"""
    products_list = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Filtering
    category_slug = request.GET.get('category')
    if category_slug:
        products_list = products_list.filter(category__slug=category_slug)
    
    price_range = request.GET.get('price_range')
    if price_range and price_range != 'all':
        if price_range == '0-500':
            products_list = products_list.filter(price__lte=500)
        elif price_range == '500-2000':
            products_list = products_list.filter(price__gte=500, price__lte=2000)
        elif price_range == '2000-5000':
            products_list = products_list.filter(price__gte=2000, price__lte=5000)
        elif price_range == '5000+':
            products_list = products_list.filter(price__gte=5000)
    
    # Sorting
    sort_by = request.GET.get('sort_by', 'name')
    if sort_by == 'price-low':
        products_list = products_list.order_by('price')
    elif sort_by == 'price-high':
        products_list = products_list.order_by('-price')
    elif sort_by == 'featured':
        products_list = products_list.order_by('-is_featured', 'name')
    else:
        products_list = products_list.order_by('name')
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'products': products_page,
        'categories': categories,
        'current_category': category_slug,
        'current_price_range': price_range,
        'current_sort': sort_by,
        'search_query': search_query,
    }
    return render(request, 'ecommerce/products.html', context)

def product_detail(request, product_id):
    """Product detail page"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'ecommerce/product_detail.html', context)

def services(request):
    """Services page"""
    services_list = Service.objects.filter(is_active=True)
    
    context = {
        'services': services_list,
    }
    return render(request, 'ecommerce/services.html', context)

def about(request):
    """About page"""
    return render(request, 'ecommerce/about.html')

def contact(request):
    """Contact page with form handling"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        # Send email notification to admin
        try:
            email_subject = f"New Contact Message: {subject}"
            email_body = render_to_string('emails/contact_form_notification.html', {
                'name': name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
                'timestamp': contact_message.created_at,
            })
            
            send_mail(
                subject=email_subject,
                message='',  # Plain text version
                html_message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send contact notification email: {e}")
        
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'ecommerce/contact.html')

def add_to_cart(request):
    """Add product to cart (AJAX)"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        
        # Get or create cart in session
        cart = request.session.get('cart', {})
        
        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id] = {
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity,
            }
        
        request.session['cart'] = cart
        request.session.modified = True
        
        # Calculate cart totals
        cart_count = sum(item['quantity'] for item in cart.values())
        cart_total = sum(item['price'] * item['quantity'] for item in cart.values())
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'cart_total': cart_total,
            'message': f'{product.name} added to cart!'
        })
    
    return JsonResponse({'success': False})

def remove_from_cart(request):
    """Remove product from cart (AJAX)"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            request.session.modified = True
        
        # Calculate cart totals
        cart_count = sum(item['quantity'] for item in cart.values())
        cart_total = sum(item['price'] * item['quantity'] for item in cart.values())
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'cart_total': cart_total
        })
    
    return JsonResponse({'success': False})

def update_cart(request):
    """Update cart item quantity (AJAX)"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart = request.session.get('cart', {})
        if product_id in cart and quantity > 0:
            cart[product_id]['quantity'] = quantity
            request.session['cart'] = cart
            request.session.modified = True
        
        # Calculate cart totals
        cart_count = sum(item['quantity'] for item in cart.values())
        cart_total = sum(item['price'] * item['quantity'] for item in cart.values())
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'cart_total': cart_total
        })
    
    return JsonResponse({'success': False})

def place_order(request):
    """Place order with MoMo payment instructions"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return JsonResponse({'success': False, 'message': 'Cart is empty'})
        
        # Get customer info
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message', '')
        
        # Create or get customer
        customer, created = Customer.objects.get_or_create(
            phone=phone,
            defaults={'name': name}
        )
        if not created:
            customer.name = name
            customer.save()
        
        # Calculate totals
        subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
        total_amount = subtotal  # No shipping for now
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            subtotal=subtotal,
            total_amount=total_amount,
            customer_notes=message
        )
        
        # Create order items
        for product_id, item in cart.items():
            product = Product.objects.get(pk=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price_at_purchase=item['price']
            )
        
        # Send email notification to admin
        try:
            email_subject = f"New Order #{order.id} - GH₵ {total_amount}"
            email_body = render_to_string('emails/new_order_notification.html', {
                'order': order,
            })
            
            send_mail(
                subject=email_subject,
                message='',  # Plain text version
                html_message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send order notification email: {e}")
        
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'total': float(total_amount),
            'momo_number': '0597427569',
            'message': 'Order placed successfully!'
        })
    
    return JsonResponse({'success': False})

def search_products(request):
    """Search products (AJAX)"""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(short_description__icontains=query) |
        Q(brand__icontains=query),
        is_active=True
    )[:10]
    
    results = []
    for product in products:
        results.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'short_description': product.short_description,
            'url': product.get_absolute_url(),
        })
    
    return JsonResponse({'results': results})

def admin_login_redirect(request):
    """Redirect to admin login"""
    from django.shortcuts import redirect
    return redirect('/admin/')

