"""scms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, static
from django.contrib import admin
from django.conf import settings



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^base/', include('common_data.urls', namespace='base')),
    url(r'^invoicing/', include("invoicing.urls", namespace="invoicing")),
    url(r'^accounting/', include("accounting.urls", namespace="accounting")),
    url(r'^staff/', include("staff.urls", namespace="staff")),
    url(r'^library/', include("library.urls", namespace="library")),
    url(r'^events/', include("events.urls", namespace="events")),
    url(r'^students/', include("students.urls", namespace="students")),
    url(r'^parents/', include("parents.urls", namespace="parents")),
    url(r'^inventory/', include("inventory.urls", namespace="inventory")),
    url(r'^shopping/', include("shopping.urls", namespace="shopping")),
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
