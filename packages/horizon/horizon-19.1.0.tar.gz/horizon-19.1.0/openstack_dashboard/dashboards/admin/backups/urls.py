# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf.urls import url

from openstack_dashboard.dashboards.admin.backups import views


urlpatterns = [
    url(r'^$', views.AdminBackupsView.as_view(), name='index'),
    url(r'^(?P<backup_id>[^/]+)/$',
        views.AdminBackupDetailView.as_view(),
        name='detail'),
    url(r'^(?P<backup_id>[^/]+)/restore/$',
        views.AdminRestoreBackupView.as_view(),
        name='restore'),
    url(r'^(?P<backup_id>[^/]+)/update_status$',
        views.UpdateStatusView.as_view(),
        name='update_status'),
]
