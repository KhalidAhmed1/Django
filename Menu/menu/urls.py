from django.urls import path
from menu.views import food_catalog

urlpatterns = [
    path('', food_catalog, name='food_catalog'),
]
