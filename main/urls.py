from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:search>', views.search, name='search'),
    path('action', views.action, name='action'),
]