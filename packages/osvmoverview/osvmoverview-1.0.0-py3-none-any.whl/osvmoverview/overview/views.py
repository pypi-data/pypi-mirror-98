from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from horizon import exceptions
from horizon import tables
from horizon import tabs

from openstack_dashboard import api
from vmoverview.overview \
    import tables as project_tables
from vmoverview.overview \
    import tabs as project_tabs

import requests

endpoint = getattr(settings, 'OPENSTACK_SERVICE_OVERVIEW', {'url': 'http://127.0.0.1:9999'})['url']

class Hyp(object):
    def __init__(self, json_def):
        for key in list(json_def.keys()):
            setattr(self, key, json_def[key])

class AdminIndexView(tabs.TabbedTableView):
    tab_group_class = project_tabs.HypervisorHostTabs
    template_name = 'vmoverview/overview/index.html'
    page_title = _("All Hypervisors")

    def get_context_data(self, **kwargs):
        context = super(AdminIndexView, self).get_context_data(**kwargs)
        try:
            stats = requests.get(endpoint + '/api/stats').json()
            #context["stats"] = api.nova.hypervisor_stats(self.request)
            context["stats"] = Hyp(stats)
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve hypervisor statistics.'))

        return context


class AdminDetailView(tables.DataTableView):
    table_class = project_tables.AdminHypervisorInstancesTable
    template_name = 'vmoverview/overview/detail.html'
    page_title = _("Servers")

    def get_data(self):
        instances = []
        '''
        try:
            id, name = self.kwargs['hypervisor'].split('_', 1)
            #result = api.nova.hypervisor_search(self.request,
            #                                    name)
            result = []
            for hypervisor in result:
                if str(hypervisor.id) == id:
                    try:
                        instances += hypervisor.servers
                    except AttributeError:
                        pass
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve hypervisor instances list.'))
        '''
        return instances

    def get_context_data(self, **kwargs):
        context = super(AdminDetailView, self).get_context_data(**kwargs)
        hypervisor_name = self.kwargs['hypervisor'].split('_', 1)[1]
        breadcrumb = [(hypervisor_name, None)]
        context['custom_breadcrumb'] = breadcrumb
        return context

