from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/all", views.products, name="products"),
    path("product/<int:product_id>/show/", views.product_show, name="product_show"),
    path("product/<int:product_id>/delete/", views.comment_delete, name="comment_delete"),

]