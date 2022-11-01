from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from home.models import Product
from .cart import Cart
from .forms import CartAddForm, CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime
# Create your views here.
from .models import Order, OrderItem, Coupon


class CartView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request, 'orders/cart.html', context={'cart': cart})


class CartAddView(View):
    # permission_required = 'orders.add_order'

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=kwargs['pk'])
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('order:cart')


class CartRemoveView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=kwargs['pk'])
        cart.remove(product)
        return redirect('order:cart')


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['pk'])
        return render(request, 'orders/order.html', context={'order': order, 'form': self.form_class})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()
        return redirect('order:order_detail', order.id)


class CouponApplyView(View):
    form_class = CouponApplyForm

    def post(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code,valid_from__lte=now,valid_to__gte=now,active=True)
            except Coupon.DoesNotExist :
                messages.error(request,'this coupon does not exists','danger')
                return redirect('order:order_detail', kwargs['pk'])
        order = Order.objects.get(id=kwargs['pk'])
        order.discount = coupon.discount
        order.save()
        return redirect('order:order_detail',kwargs['pk'])
