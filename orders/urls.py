from django.urls import path
from .views import *

app_name = 'order'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('cart/',CartView.as_view(),name='cart'),
    path('cart/add/<int:pk>/',CartAddView.as_view(),name='cart_add'),
    path('cart/remove/<int:pk>/',CartRemoveView.as_view(),name='cart_remove'),
    path('apply/<int:pk>/',CouponApplyView.as_view(),name='apply_coupon'),
]