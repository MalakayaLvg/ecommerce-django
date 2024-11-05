from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/all", views.products, name="products"),
    path("product/<int:product_id>/show/", views.product_show, name="product_show"),
    path("product/<int:product_id>/delete/", views.comment_delete, name="comment_delete"),

    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.create_checkout_session, name='checkout'),
    path('success/',views.success_view, name="success_view"),
    path('cancel/',views.cancel_view, name="cancel_view"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)