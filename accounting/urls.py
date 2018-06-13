from django.conf.urls import url
import views
from rest_framework import routers

tax_router = routers.DefaultRouter()
tax_router.register(r'^api/tax', views.TaxViewset)

urlpatterns =[
    url(r'^$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^create-transaction/?$', views.TransactionCreateView.as_view(), 
        name='create-transaction'),
    url(r'^transaction-update/(?P<pk>[\w]+)/?$', 
        views.TransactionUpdateView.as_view(), name='transaction-update'),
    url(r'^transaction-delete/(?P<pk>[\w]+)/?$', 
        views.TransactionDeleteView.as_view(), name='transaction-delete'),
    url(r'^create-account/?$', views.AccountCreateView.as_view(), 
        name='create-account'),
    url(r'^account-detail/(?P<pk>[\w]+)/?$', views.AccountDetailView.as_view(), 
        name='account-detail'),
    url(r'^account-update/(?P<pk>[\w]+)/?$', views.AccountUpdateView.as_view(), 
        name='account-update'),
    url(r'^account-list/?$', views.AccountListView.as_view(), 
        name='account-list'),
    url(r'^create-journal/?$', views.JournalCreateView.as_view(), 
        name='create-journal'),
    url(r'^journal-list/?$', views.JournalListView.as_view(), 
        name='journal-list'),
    url(r'^journal-detail/(?P<pk>[\w]+)/?$', views.JournalDetailView.as_view(), 
        name='journal-detail')
] + tax_router.urls