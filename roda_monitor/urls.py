"""roda_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, re_path
from monitor_backend import views, views_n2n, views_sink_source

urlpatterns = [
    # path('admin/', admin.site.urls),
    # n2n
    path('api/n2n/registry', views_n2n.n2n_registry),
    path('api/n2n/update', views_n2n.n2n_update),
    path('api/n2n/delete', views_n2n.n2n_delete),
    path('api/n2n/list', views_n2n.n2n_list),
    path('api/n2n/topo', views_n2n.n2n_topo),

    # sink and source
    path('api/sink_source/registry', views_sink_source.sink_source_registry),
    path('api/sink_source/update', views_sink_source.sink_source_update),
    path('api/sink_source/delete', views_sink_source.sink_source_delete),
    path('api/sink_source/list', views_sink_source.sink_source_list),
    path('api/sink_source/topo', views_sink_source.sink_source_topo),

    path('api/getMatchTime', views.getMatchTime),
    path('api/getSubMatchTime', views.getSubMatchTime),
    re_path(r'^.*$', views.index_fun)
]
