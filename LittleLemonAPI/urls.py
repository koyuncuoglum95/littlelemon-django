from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category-list'),
    path('menu-items/', views.menuitem_list, name='menuitem-list'),
    path('menu-items/<int:pk>/', views.menuitem_detail, name='menuitem-detail'),
    path('cart/', views.cart_list, name='cart-list'),
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),
    path('delivery-orders/<int:pk>/', views.delivery_order_detail, name='delivery-order-detail'),
    path('delivery-orders/', views.delivery_crew_orders, name='delivery-crew-orders'),
    path('categories/<int:category_id>/menu-items/', views.category_menuitems, name='category-menuitems'),
    path('menu-items/paginate/', views.paginate_menuitems, name='paginate-menuitems'),
    path('menu-items/sort-by-price/', views.sort_menuitems_by_price, name='sort-menuitems-by-price'),
    path('users/<int:user_id>/assign-group/', views.assign_user_to_group, name='assign-user-to-group'),
    path('orders/<int:order_id>/assign-delivery-crew/', views.assign_order_to_delivery_crew, name='assign-order-to-delivery-crew'),
    path('menu-items/<int:menuitem_id>/set-item-of-the-day/', views.set_item_of_the_day, name='set-item-of-the-day'),
]
