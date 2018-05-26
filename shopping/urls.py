from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.ShoppingHome.as_view(), name="home"),
]