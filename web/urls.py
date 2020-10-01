from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('term-and-conditions/', terms_and_conditions, name="term"),
    path('privacy-policy/', privacy_policy, name="privacy"),
]
