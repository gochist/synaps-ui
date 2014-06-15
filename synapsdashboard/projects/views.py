import logging

import boto

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import tabs
from horizon import views
from horizon.utils import memoized

from synapsdashboard.projects import tables as project_tables
from synapsdashboard.projects import tabs as project_tabs
from synapsdashboard.projects import forms as project_forms

from openstack_dashboard import api

import logging

LOG = logging.getLogger(__name__)
cw = boto.connect_cloudwatch()


class GraphView(forms.ModalFormView):
    form_class = project_forms.GraphForm
    template_name = 'synapsdashboard/projects/graph.html'
#     success_url = reverse_lazy('horizon:synapsdashboard:projects:metrics')

    def get_context_data(self, **kwargs):
        context = super(GraphView, self).get_context_data(**kwargs)
#         context['tenant_id'] = tenant_id
        return context

#     def get_initial(self):
#         return {'instance_id': self.kwargs['instance_id']}




class MonitoringView(tabs.TabbedTableView):
    tab_group_class = project_tabs.MonitoringTabs
    template_name = 'synapsdashboard/projects/monitoring.html'
    
    def get_context_data(self, tenant_id, **kwargs):
        context = super(MonitoringView, self).get_context_data(**kwargs)
        project = api.keystone.tenant_get(self.request, tenant_id, admin=True)
        context['project'] = project
        context['tenant_id'] = tenant_id
        return context



class IndexView(tables.DataTableView):
    table_class = project_tables.TenantsTable
    template_name = 'synapsdashboard/projects/index.html'

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        tenants = []
        marker = self.request.GET.get(
            project_tables.TenantsTable._meta.pagination_param, None)
        domain_context = self.request.session.get('domain_context', None)
        try:
            tenants, self._more = api.keystone.tenant_list(
                self.request,
                domain=domain_context,
                paginate=True,
                marker=marker)
        except Exception:
            self._more = False
            exceptions.handle(self.request,
                              _("Unable to retrieve project list."))
        return tenants

