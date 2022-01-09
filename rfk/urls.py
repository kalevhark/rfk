"""rfk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cookies/', include('cookie_consent.urls')),
    path('sandbox/', views.sandbox, name='sandbox'),
    path('covidpass_s9a/', views.covidpass_s9a, name='covidpass_s9a'),
    path('kysimustik2/', views.kysimustik2, name='kysimustik2'),
    path('kysimustik3/', views.kysimustik3, name='kysimustik3'),
    path('kysimustik4/', views.kysimustik4, name='kysimustik4'),
    path('kysimustik5/', views.kysimustik5, name='kysimustik5'),
    path('some_view/', views.some_view, name='some_view'),
    path('main/', include('main.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)