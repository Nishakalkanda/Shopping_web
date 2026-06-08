from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
import razorpay
from Products.models import Product
from cart.models import Address, Cart, CartItem, Order, OrderItem
from ecommerce import settings

# Create your views here.


def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    items =  CartItem.objects.filter(cart=cart)
    total = sum(
        item.quantity * item.product.price
        for item in items
    )
    
    return render(request, 'cart.html', {
        'items':items,
        'total': total
    })
    
    
def add_to_cart(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created =CartItem.objects.get_or_create(cart=cart, product = product)
    
    if not created:
        item.quantity += 1
        item.save()
        
    return redirect('cart')   


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id = item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    
    return redirect('cart')


def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    item.quantity += 1
    item.save()

    return redirect('cart')


def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


def place_order(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    
    total = sum(item.quantity*item.product.price for item in items)
    order = Order.objects.create(user=request.user, total_amount=total)
    
    for item in items:
        OrderItem.objects.create(order=order, product=item.product,quantity=item.quantity, price = item.product.price)
        
    CartItem.objects.filter(cart=cart)
    
    return redirect('orders')


def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'orders.html', {'orders':orders})

    
def delete_all_orders(request):
    Order.objects.filter(user=request.user).delete()

    return redirect('orders')    


# def payment_page(request):
#     cart_items = CartItem.objects.all()

#     total = sum(item.product.price * item.quantity for item in cart_items)

#     return render(
#         request,
#         'payment.html',
#         {'total': total}
#     )

@login_required
def payment_page(request):
    cart = Cart.objects.get(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, 
                                   settings.RAZORPAY_KEY_SECRET))
    
    payment = client.order.create({
        "amount" : int(total * 100),
        "currency" : "INR",
        "payment_capture" : 1
    })
        
    return render(request, "payment.html",
                  {
                      "payment" : payment,
                      "total" : total,
                      "razorpay_key" : settings.RAZORPAY_KEY_ID
                  })

@login_required
def payment_success(request):
    cart = Cart.objects.get(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)
    
    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    Order.objects.create(
        user=request.user,
        total_amount=total,
        status='Pending'
    )

    cart_items.delete()

    return redirect('orders')



     
@login_required
def address_page(request):

    if request.method == "POST":

        Address.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            phone=request.POST['phone'],
            address=request.POST['address_line'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode']
        )

        return redirect('payment_page')

    return render(request, 'address.html')     