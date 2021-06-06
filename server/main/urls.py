from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:search>', views.search, name='search'),
    path('show_plugins', views.show_plugins, name='show_plugins'),
    path('action', views.action, name='action'),
]