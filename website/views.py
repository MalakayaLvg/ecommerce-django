from django.shortcuts import render, get_object_or_404

from website.models import Product


# Create your views here.

def index(request):
    return render(request, "website/home.html")

def products(request):
    products_all = Product.objects.all()
    context = {"products":products_all}
    return render(request,"product/index.html",context)

def product_show(request,product_id):
    product = get_object_or_404(Product,pk=product_id)
    context = {"product":product}
    return render(request,"product/show.html",context)