from django.urls import path
from . import views

urlpatterns = [
	path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('add-product/', views.add_product, name='add_product'),
    path('product-list/', views.product_list, name='product_list'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('update-product/<int:pk>/', views.update_product, name='update_product'),
    path('order-list/', views.order_list, name='order_list'),
    path('order-list/<int:order_id>/update/',views. update_order_status, name='update_order'),
	
]
