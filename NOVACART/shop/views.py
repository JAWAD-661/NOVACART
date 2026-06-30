from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, OrderItem, Product


def seed_products():
    sample_products = [
        {
            'name': 'Aurora Headphones',
            'description': 'Immersive sound with a comfortable over-ear design for long study sessions.',
            'price': Decimal('89.99'),
            'category': 'Audio',
            'stock': 12,
        },
        {
            'name': 'Nova Smartwatch',
            'description': 'Track your workouts and stay connected with a sleek health-focused display.',
            'price': Decimal('129.50'),
            'category': 'Wearables',
            'stock': 8,
        },
        {
            'name': 'Lumen Laptop Stand',
            'description': 'A sturdy, adjustable stand that improves posture and saves desk space.',
            'price': Decimal('44.00'),
            'category': 'Accessories',
            'stock': 15,
        },
        {
            'name': 'Echo Bluetooth Speaker',
            'description': 'Portable rich bass speaker perfect for home parties and travel.',
            'price': Decimal('59.90'),
            'category': 'Audio',
            'stock': 10,
        },
    ]
    for item in sample_products:
        Product.objects.get_or_create(name=item['name'], defaults=item)


def home(request):
    if not Product.objects.exists():
        seed_products()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = Product.objects.filter(
            name__icontains=search_query
        ) | Product.objects.filter(
            description__icontains=search_query
        )
    else:
        products = Product.objects.all()
    
    return render(request, 'shop/home.html', {'products': products, 'search_query': search_query})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})


def get_cart(request):
    return request.session.get('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def cart(request):
    cart_items = []
    total = Decimal('0.00')
    cart_data = get_cart(request)

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        cart_data = get_cart(request)
        quantity = max(1, int(request.POST.get('quantity', 1)))
        cart_data[str(product_id)] = cart_data.get(str(product_id), 0) + quantity
        save_cart(request, cart_data)
        messages.success(request, f'{product.name} added to your cart.')
    return redirect('cart')


def update_cart(request, product_id):
    if request.method == 'POST':
        cart_data = get_cart(request)
        quantity = max(0, int(request.POST.get('quantity', 0)))
        if quantity <= 0:
            cart_data.pop(str(product_id), None)
        else:
            cart_data[str(product_id)] = quantity
        save_cart(request, cart_data)
        messages.info(request, 'Your cart has been updated.')
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart_data = get_cart(request)
    cart_data.pop(str(product_id), None)
    save_cart(request, cart_data)
    messages.info(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def checkout(request):
    cart_data = get_cart(request)
    if not cart_data:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    cart_items = []
    total = Decimal('0.00')
    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        zip_code = request.POST.get('zip_code', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not all([customer_name, address, city, zip_code, phone]):
            messages.error(request, 'Please complete all shipping details.')
            return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total})

        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            address=address,
            city=city,
            zip_code=zip_code,
            phone=phone,
            total=total,
        )
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], price=item['product'].price)
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, 'Order placed successfully!')
        return redirect('order_success', order_id=order.id)

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'shop/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'shop/my_orders.html', {'orders': orders})


@user_passes_test(lambda user: user.is_staff)
def admin_orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        if order_id and status:
            order = get_object_or_404(Order, pk=order_id)
            order.status = status
            order.save(update_fields=['status'])
            messages.success(request, f'Order #{order.id} updated to {status}.')
        return redirect('admin_orders')

    orders = Order.objects.all().prefetch_related('items__product').order_by('-created_at')
    return render(request, 'shop/admin_orders.html', {'orders': orders})


def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out. Welcome back!')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
