from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('naase/', views.naase, name='naase'),
    path('teavita/', views.teavita, name='teavita'),
    path('get_order/', views.get_order, name='get_order'),
]

