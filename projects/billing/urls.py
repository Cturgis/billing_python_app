from django.urls import path
from .views import auth_views, customer_views, product_views

app_name = 'billing'

urlpatterns = [
    # Auth URLs
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('dashboard/', auth_views.dashboard, name='dashboard'),

    # Customer URLs
    path('clients/', customer_views.customer_list, name='customer_list'),
    path('clients/nouveau/', customer_views.customer_create, name='customer_create'),
    path('clients/<int:pk>/modifier/', customer_views.customer_update, name='customer_update'),
    path('clients/<int:pk>/supprimer/', customer_views.customer_delete, name='customer_delete'),

    # Product URLs
    path('produits/', product_views.product_list, name='product_list'),
    path('produits/nouveau/', product_views.product_create, name='product_create'),
    path('produits/<int:pk>/modifier/', product_views.product_update, name='product_update'),
    path('produits/<int:pk>/supprimer/', product_views.product_delete, name='product_delete'),
    path('produits/<int:pk>/increment/', product_views.product_increment, name='product_increment'),
    path('produits/<int:pk>/decrement/', product_views.product_decrement, name='product_decrement'),
    path('produits/<int:pk>/update-qtty/', product_views.product_update_qtty, name='product_update_qtty'),
    path('produits/<int:pk>/update-price/', product_views.product_update_price, name='product_update_price'),

    # Customer dashboard URLs
    path('customer/dashboard/', customer_views.customer_dashboard, name='customer_dashboard'),
    path('customer/boutique/', customer_views.shop_view, name='shop'),
    path('customer/mes-factures/', customer_views.my_invoice_view, name='my_invoice'),
    path('customer/buy/<int:product_id>/', customer_views.buy_product_view, name='buy_product'),
]