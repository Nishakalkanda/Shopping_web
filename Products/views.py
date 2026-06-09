from django.shortcuts import get_object_or_404, render, redirect
from requests import request
from rest_framework.response import Response
from django.core.mail import send_mail
from Products.serializers import ProductSerializer
from cart.models import Review
from .models import Product, Wishlist
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view


# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'products.html', {'products': products})


def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    reviews = Review.objects.filter(product=product).order_by('-created_at')

    return render(
        request,
        'product_detail.html',
        {
            'product': product,
            'reviews': reviews
        }
    )
    
    
def product_list(request):
    query = request.GET.get('q')
    
    if query:
        products = Product.objects.filter(name__icontains=query)
        
    else:
        products = Product.objects.all()
        
    return render(
        request,
        'products.html',
        {'products': products}
    )
    
    
@login_required
def add_to_wishlist(request, product_id):

    product = Product.objects.get(id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('wishlist')   


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(
        request,
        'wishlist.html',
        {'wishlist_items': wishlist_items}
    )
    
 
@api_view(['GET'])    
def product_api(request):
    products = Product.objects.all()
    
    serializer = ProductSerializer(products, many = True)
    
    return Response(serializer.data)
        
        

    
@login_required
def add_review(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.method == "POST":
        rating = request.POST.get('rating')
        
        comment = request.POST.get('comment')
        
        Review.objects.create(user = request.user, product = product, rating=rating, comment = comment)
        
    return redirect('product_detail', id = product.id) 

        