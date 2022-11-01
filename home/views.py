from django.shortcuts import render , get_object_or_404
from django.views import View

from orders.forms import CartAddForm
from .models import Product  ,Category

# Create your views here.


class HomeView(View):
    def get(self,request,*args,**kwargs):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if 'slug' in kwargs:
            category = Category.objects.get(slug=kwargs['slug'])
            products = products.filter(category=category)
        return render(request, 'home/home.html',context={'products':products,'categories':categories})


class ProductDetailView(View):
    form_class_cart = CartAddForm
    def get(self,request,*args,**kwargs):
        product = get_object_or_404(Product,slug = kwargs['slug'])
        form = self.form_class_cart
        return render(request,'home/detail.html',context={'product':product,'form':form})

