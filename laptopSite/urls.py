from django.contrib import admin
from django.urls import path
from CustomerSite.views import *
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.conf import settings
from django.urls import reverse
urlpatterns = [
    path("",home,name="home"),
    path("admin/",admin,name="admin"),
    path("home/",home,name="home"),
    path('laptops/', LaptopListView.as_view(), name='laptop_list'),
    path('laptops/<int:pk>/', LaptopDetailView.as_view(), name='laptop_detail'),
    path('add_to_cart/<int:laptop_id>/<int:price>/<int:quantity>/<int:ram>/<int:ssd>', add_to_cart, name='add_to_cart'),
    path('cart/',CartListView.as_view(), name='cart_list'),
    path('subtract_quantity_cart/<int:pk>/',subtract_quantity_cart, name='subtract_quantity_cart'),
    path('add_quantity_cart/<int:pk>/',add_quantity_cart, name='add_quantity_cart'),
    path('remove_item_on_cart/<int:pk>/',  remove_from_cart, name='remove_from_cart'),
    path('add_laptop/', add_laptop, name='add_laptop'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('edit_laptop/<int:pk>/', edit_laptop, name='edit_laptop'),
    path('edit_images/<int:pk>/', edit_images, name='edit_images'),
    path('edit_image/<int:pk>/', edit_image, name='edit_image'),
    path('delete_laptop/<int:pk>/',delete_laptop , name='delete_laptop'),
    path('directToPage/<int:stt>',directLink,name='directToPage'),
    path('directToPage/<int:stt>',directLink,name='directToPage'),
    path('create_payment/<int:pk>', create_payment, name='create_payment'),
    path('execute_payment/', execute_payment, name='execute_payment'),
    path('cancel_payment/', cancel_payment, name='cancel_payment'),
    path('checkout/', checkout, name='checkout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = page_not_found
