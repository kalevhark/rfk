from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_icf_calcs/', views.get_icf_calcs, name='get_icf_calcs'),
    path('get_icf_path/', views.get_icf_path, name='get_icf_path'),
    path('get_icf_summary/', views.get_icf_summary, name='get_icf_summary')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)