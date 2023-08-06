# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from horizon import exceptions
from horizon import tabs
from horizon.utils import functions as utils

from openstack_dashboard.api import nova
from openstack_dashboard.dashboards.admin.hypervisors.compute \
    import tabs as cmp_tabs
#from openstack_dashboard.dashboards.admin.hypervisors import tables
from vmoverview.overview import tables

import requests

endpoint = getattr(settings, 'OPENSTACK_SERVICE_OVERVIEW', {'url': 'http://127.0.0.1:9999'})['url']

class Hyp(object):
    def __init__(self, json_def):
        for key in list(json_def.keys()):
            setattr(self, key, json_def[key])


class HypervisorFlavorTab(tabs.TableTab):
    table_classes = (tables.AdminFlavorHypervisorsTable,)
    name = _("Available flavors")
    slug = "hypervisorflavor"
    template_name = "horizon/common/_detail_table.html"

    def get_hypervisorsflavor_data(self):
        hypervisors = []
        try:
            #hypervisors = nova.hypervisor_list(self.request)
            hypervisors = []
            hypervisors_json = requests.get(endpoint + '/api/hypervisors').json()
            for hj in hypervisors_json['flavors']:
                hypervisors.append(Hyp(hj))
            hypervisors.sort(key=utils.natural_sort('name'))
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve hypervisor flavors information.'))

        return hypervisors


class HypervisorTab(tabs.TableTab):
    table_classes = (tables.AdminHypervisorsTable,)
    name = _("Hypervisor")
    slug = "hypervisor"
    template_name = "horizon/common/_detail_table.html"

    def get_hypervisors_data(self):
        hypervisors = []
        try:
            #hypervisors = nova.hypervisor_list(self.request)
            hypervisors = []
            hypervisors_json = requests.get(endpoint + '/api/hypervisors').json()
            for hj in hypervisors_json['hypervisors']:
                hypervisors.append(Hyp(hj)) 
            hypervisors.sort(key=utils.natural_sort('hypervisor_hostname'))
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve hypervisor information.'))

        return hypervisors


class HypervisorHostTabs(tabs.TabGroup):
    slug = "hypervisor_info"
    tabs = (HypervisorTab, HypervisorFlavorTab,)
    sticky = True
