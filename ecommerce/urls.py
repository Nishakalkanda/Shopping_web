"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Products.views import add_review, add_to_wishlist, product_api, product_detail, product_list, wishlist_view
from authentication.views import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from cart import views
from cart.views import add_to_cart, cart_view, decrease_quantity, delete_all_orders, increase_quantity, order_detail, orders_view, place_order, remove_from_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect),
    path('home/', home, name="home"),
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register'),
    path('products/', product_list, name='product_list'),
    path('products/<int:id>/', product_detail, name='product_detail'),
    path('cartt/', cart_view, name='cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('increase/<int:item_id>/', increase_quantity,name='increase_quantity'),
    path('decrease/<int:item_id>/', decrease_quantity, name='decrease_quantity'),
    path('place-order/', place_order, name='place_order'),
    path('orders/', orders_view, name='orders'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('delete-all-orders/', delete_all_orders, name='delete_all_orders'),
    path('payment/', views.payment_page, name = 'payment_page'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('address/', views.address_page, name='address_page'),
    path('api/products/', product_api, name = 'product_api'),
    path('review/<int:product_id>/', add_review, name = 'add_review'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
    
    
