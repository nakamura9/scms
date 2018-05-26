from django.shortcuts import render

from django.views.generic import TemplateView
import os

class Test(TemplateView):
    template_name = os.path.join("common_data", "test.html")

class ReactTest(TemplateView):
    template_name = os.path.join("common_data", "react_test.html")