from django.conf.urls import url
import views
from rest_framework.routers import DefaultRouter

item_router = DefaultRouter()
item_router.register(r'api/item', views.ItemAPIViewSet, base_name='item')

customer_router = DefaultRouter()
customer_router.register(r'api/customer', views.CustomerAPIViewSet, base_name='customer')

invoice_router = DefaultRouter()
invoice_router.register(r'api/invoice', views.InvoiceAPIViewSet, base_name='invoice')

payment_router = DefaultRouter()
payment_router.register(r'api/payment', views.PaymentAPIViewSet, base_name='payment')

sales_rep_router = DefaultRouter()
sales_rep_router.register(r'api/sales-rep', views.SalesRepsAPIViewSet, base_name='sales-rep')

account_router = DefaultRouter()
account_router.register(r'api/account', views.AccountAPIViewSet, base_name='account')

urlpatterns = [
    url(r'^$', views.Home.as_view(), name="home"),
    url(r'^create-item$', views.ItemCreateView.as_view(), name='create-item'),
    url(r'^update-item/(?P<pk>[\w]+)$', views.ItemUpdateView.as_view(), name='update-item'),
    url(r'^item-list$', views.ItemListView.as_view(), name='items-list'),
    url(r'^create-customer$', views.CustomerCreateView.as_view(), name='create-customer'),
    url(r'^update-customer/(?P<pk>[\w]+)$', views.CustomerUpdateView.as_view(), name='update-customer'),
    url(r'^customer-list$', views.CustomerListView.as_view(), name='customers-list'),
    url(r'^create-sales-rep$', views.SalesRepCreateView.as_view(), name='create-sales-rep'),
    url(r'^update-sales-rep/(?P<pk>[\w]+)$', views.SalesRepUpdateView.as_view(), name='update-sales-rep'),
    url(r'^sales-reps-list$', views.SalesRepListView.as_view(), name='sales-reps-list'),
    url(r'^invoices-list$', views.InvoiceListView.as_view(), name='invoices-list'),
    url(r'^create-invoice$', views.InvoiceCreateView.as_view(), name='create-invoice'),
    url(r'^update-invoice/(?P<pk>[\w]+)$', views.InvoiceUpdateView.as_view(), name='update-invoice'),
] + item_router.urls + customer_router.urls + invoice_router.urls + \
    payment_router.urls + sales_rep_router.urls + account_router.urls