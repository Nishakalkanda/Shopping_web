from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Wishlist
from django.contrib.auth.decorators import login_required


# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'products.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product':product})

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