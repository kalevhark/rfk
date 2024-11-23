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
from ajax_select import urls as ajax_select_urls

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import django_filters
from django_filters import rest_framework as filters

from rest_framework import routers, serializers, viewsets

from main import views
from main.models import RFK

# Serializers define the API representation.
class RFKSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RFK
        fields = ['code', 'Translated_title', 'Translated_description', 'Translated_inclusions', 'Translated_exclusions']


class RFKFilter(filters.FilterSet):
    # Võimaldab API päringuid: http://18.196.203.237/api/rfk/?code=d450
    # code_search = django_filters.CharFilter(field_name='code', lookup_expr='exact')
    code = django_filters.CharFilter(method='lookup_code')

    def lookup_code(self, queryset, field_name, value):
        queryset = queryset.filter(code=value)
        return queryset


# ViewSets define the view behavior.
class RFKViewSet(viewsets.ModelViewSet):
    queryset = RFK.objects.all()
    serializer_class = RFKSerializer
    # Järgnev vajalik, et saaks teha filtreeritud API päringuid
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RFKFilter
    
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'rfk', RFKViewSet)

urlpatterns = [
    path('', views.rfk, name='index'),
    path('api/', include(router.urls)),
    path('ajax_select/', include(ajax_select_urls)),
    path('privacy/', views.privacy, name='privacy'),
    path('sandbox/', views.sandbox, name='sandbox'),
    path('rfk/', views.rfk, name='rfk'),
    path('coreset/', views.coreset, name='coreset'),
    path('prt/', views.prt, name='prt'),
    path('expmoodul/', views.expmoodul, name='expmoodul'),
    # path('prt1/', views.prt1, name='prt1'),
    path('covidpass_s9a/', views.covidpass_s9a, name='covidpass_s9a'),
    path('covidpass_s9a_2/', views.covidpass_s9a_2, name='covidpass_s9a_2'),
    # path('kysimustik2/', views.kysimustik2, name='kysimustik2'),
    # path('kysimustik3/', views.kysimustik3, name='kysimustik3'),
    # path('kysimustik4/', views.kysimustik4, name='kysimustik4'),
    # path('kysimustik5/', views.kysimustik5, name='kysimustik5'),
    # path('kysimustik6/', views.kysimustik6, name='kysimustik6'),
    path('kysimustik7/', views.kysimustik7, name='kysimustik7'),
    path('kysimustik8/', views.kysimustik8, name='kysimustik8'),
    path('kysimustik9/', views.kysimustik9, name='kysimustik9'),
    path('some_view/', views.some_view, name='some_view'),
    path('main/', include('main.urls')),
    path('montonio/', include('montonio.urls')),
    path('sihtnumber/', include('sihtnumber.urls')),
    # path('j6ul2023/', views.j6ul2023, name='j6ul2023'),
    path('helenamiia/', views.helenamiia, name='helenamiia'),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)