from django.contrib import admin
from django.urls import path
from . import views    

urlpatterns = [
    path('login/', views.login_page ,name='login'),
    path('logout/', views.logout_page ,name='logout'),
    path('register/', views.register ,name='register'),
    path('profile/', views.profile ,name='profile'),
    path('', views.home , name='home'),
    path('shop/', views.shop , name='shop'),
    path('product/<int:id>/', views.product, name='product'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('cart/<int:id>/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('ordercompleted/', views.ordercompleted, name='ordercompleted'),
]