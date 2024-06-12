from django.urls import path
from . import views

urlpatterns = [
    path('advisories/', views.advisories, name='advisories'),
     path('map/', views.map, name='map'),
]