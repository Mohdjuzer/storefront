from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem

# Create your views here.
def say_hello(request):
    query_set = Product.objects.values('title','id', 'orderitem__product_id').order_by('title')
    query_set1 = OrderItem.objects.values('product__title').order_by('product__title')
    return render(request, 'hello.html', {'name': 'Mohammed', 'products': list(query_set)})