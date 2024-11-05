from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect

from website.models import Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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
    context = {"product":product}
    return render(request,"product/show.html",context)