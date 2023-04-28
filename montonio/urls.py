from django.urls import path

from . import views

app_name = 'montonio'

urlpatterns = [
    path('', views.index, name='index'),
    path('anneta1', views.anneta1, name='anneta1'),
    path('anneta2', views.anneta2, name='anneta2'),
    path('naase/<str:merchantReference>/', views.naase, name='naase'),
    path('teavita/', views.teavita, name='teavita'),
    path('get_order/', views.get_order, name='get_order'),
]

