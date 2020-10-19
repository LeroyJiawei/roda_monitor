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
from monitor_backend import views, views_network, views_systems, views_hub, views_filter

urlpatterns = [
    # path('admin/', admin.site.urls),
    # network
    path('api/network/is_overlay', views_network.network_is_overlay),
    path('api/network/set_overlay', views_network.network_set_overlay),
    path('api/network/registry', views_network.network_registry),
    path('api/network/update', views_network.network_update),
    path('api/network/delete', views_network.network_delete),
    path('api/network/list', views_network.network_list),
    path('api/network/topo', views_network.network_topo),

    # sink and source
    path('api/sink_source/registry', views_systems.sink_source_registry),
    path('api/sink_source/update', views_systems.sink_source_update),
    path('api/sink_source/delete', views_systems.sink_source_delete),
    path('api/sink_source/list', views_systems.sink_source_list),
    path('api/sink_source/topo', views_systems.sink_source_topo),

    # hub
    path('api/hub/info', views_hub.hub_info),
    path('api/hub/list_images', views_hub.hub_list_images),
    path('api/hub/delete_image', views_hub.hub_delete_image),
    path('api/hub/list_docker_images', views_hub.hub_list_docker_images),
    path('api/hub/run_image', views_hub.hub_run_image),
    path('api/hub/upload_file', views_hub.hub_upload_file),
    path('api/hub/list_file', views_hub.hub_list_file),
    path('api/hub/delete_file', views_hub.hub_delete_file),
    path('api/hub/upload_dockerfile', views_hub.hub_upload_dockerfile),

    # filter
    path('api/filter/list', views_filter.filter_list),
    path('api/filter/pull', views_filter.filter_pull_image),
    path('api/filter/source_images', views_filter.filter_source_images),
    path('api/filter/match_perf', views_filter.filter_get_match_perf),
    path('api/filter/end_perf', views_filter.filter_get_e2e_perf),
    path('api/filter/update_config', views_filter.filter_update_config),
    path('api/filter/delete', views_filter.filter_delete),

    re_path(r'^.*$', views.index_fun)
]
