# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
import os


class ShoppingHome(TemplateView):
    template_name = os.path.join("shopping", "home.html")