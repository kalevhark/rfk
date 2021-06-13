from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_icf_calcs/', views.get_icf_calcs, name='get_icf_calcs'),
    path('get_icf_path/', views.get_icf_path, name='get_icf_path'),
    path('get_icf_summary/', views.get_icf_summary, name='get_icf_summary')
]