from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('register', views.create, name='create'),
    path('display', views.display, name='display'),
    #path('delete', views.delete, name='delete'),
]