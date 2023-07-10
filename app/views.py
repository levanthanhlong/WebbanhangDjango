from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib import messages
# hien thi cua trang web
# Create your views here.

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    id = request.GET.get('id','')
    products = Product.objects.filter(id = id)
    categories = Category.objects.filter(is_sub = False)
    context = {'products':products,'items':items,'order':order,'cartItems':cartItems,'categories':categories}
    return render(request,'app/detail.html', context)

def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_catergory = request.GET.get('category','')
    if active_catergory:
        products = Product.objects.filter(category__slug = active_catergory)
    
    context = {'categories':categories,'products':products,'active_catergory':active_catergory}
    return render(request, 'app/category.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        products = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False)
    return render(request, 'app/search.html',{"searched": searched,"products":products,'items':items,'order':order,'cartItems':cartItems,'categories':categories})

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    categories = Category.objects.filter(is_sub = False)
    context = {'form': form, 'categories':categories}
    return render(request, 'app/register.html', context)

def loginPage(request):
    isLoggedIn = False
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password=password)
        if user is not None:
            login(request,user)
            isLoggedIn = True
            return redirect('home')
        else: messages.info(request,'user or password is not correct!')
    categories = Category.objects.filter(is_sub = False)
    context = {'categories':categories}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    response = redirect('home')
     # Xoá bộ nhớ cache
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub = False)
    context = {'products': products,'cartItems': cartItems,'categories':categories}
    return render(request,'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False)
    context = {'items':items,'order':order,'cartItems':cartItems,'categories':categories}
    return render(request,'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False)
    context = {'items':items,'order':order,'cartItems':cartItems,'categories':categories}
    return render(request,'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('added', safe=False)
