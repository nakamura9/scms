from django.conf.urls import url
import views 

urlpatterns = [
    url(r'^$', views.InventoryHome.as_view(), name="home"),
    url(r'^supplier-create/?$', views.SupplierCreateView.as_view(), name="supplier-create"),
    url(r'^supplier-list/?$', views.SupplierListView.as_view(), name="supplier-list"),
    url(r'^supplier-update/(?P<pk>[\w]+)/?$', views.SupplierUpdateView.as_view(), name="supplier-update"),
    url(r'^item-create/?$', views.ItemCreateView.as_view(), name="item-create"),
    url(r'^item-update/(?P<pk>[\w]+)/?$', views.ItemUpdateView.as_view(), name="item-update"),
    url(r'^order-create/?$', views.OrderCreateView.as_view(), name="order-create"),
    url(r'^order-list/?$', views.OrderListView.as_view(), name="order-list"),
    url(r'^order-update/?$', views.OrderListView.as_view(), name="order-list"),
]