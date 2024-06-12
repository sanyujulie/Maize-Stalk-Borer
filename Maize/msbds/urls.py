from django.urls import path
from . import views

urlpatterns = [
    path('', views.advisories, name='advisories'),
     path('map/', views.map, name='map'),
       path('notification/', views.notification, name='notification'),
]