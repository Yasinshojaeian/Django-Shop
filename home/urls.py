from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('',HomeView.as_view(),name='home' ),
    path('<slug:slug>/',ProductDetailView.as_view(),name='product_detail'),
    path('category/<slug:slug>/',HomeView.as_view(),name='category_filter'),
]