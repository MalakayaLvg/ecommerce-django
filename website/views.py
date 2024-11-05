import stripe
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from requests import session

from website.forms import CommentForm
from website.models import Product, Comment, Cart, CartItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse


# Create your views here.

def index(request):
    return render(request, "website/home.html")


################### USER ##############################
# gerard , dKc&jDFH-XWd5;:
# felix , dKc&jDFH-XWd5;:
def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect("products")
    else:
        form = UserCreationForm()
        context = {"form":form}
        return render(request,"user/signup.html",context)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("products")
    else:
        form = AuthenticationForm()
        context = {"form":form}
        return render(request,"registration/login.html",context)

def logout_view(request):
    logout(request)
    return redirect("index")






#################### PRODUCTS ##########################

def products(request):
    products_all = Product.objects.all()
    context = {"products":products_all}
    return render(request,"product/index.html",context)

def product_show(request,product_id):
    product = get_object_or_404(Product,pk=product_id)
    comments = product.comments.all()
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.product = product
                form.save()
                return redirect("product_show",product_id)
        else:
            return redirect("login")
    else:
        form = CommentForm()
        context = {"product":product,"form":form,"comments":comments}
        return render(request,"product/show.html",context)

def comment_delete(request,comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment,pk=comment_id)
        comment.delete()
        return redirect("product_show",comment.product_id)
    else:
        return redirect("login")



############### PAIEMENT #####################

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart,product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect("product_show",product_id)
    else:
        return redirect("login")

def cart_detail(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        items = cart.items.all() if cart else []
        total_amount = sum(item.product.price * item.quantity for item in items)
        context = {"cart":cart,"items":items,"total_amount":total_amount}
        return render(request,"cart/detail.html",context)

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_detail')

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()


        if not cart or not cart.items.exists():
            return redirect('cart_detail')

        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.title,
                    },
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            }
            for item in cart.items.all()
        ]

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success_view')),
            cancel_url=request.build_absolute_uri(reverse('cancel_view')),
        )
        return redirect(session.url, code=303)

def success_view(request):
    return render(request,"cart/success_payment.html")

def cancel_view(request):
    return render(request,"cart/cancel_payment.html")