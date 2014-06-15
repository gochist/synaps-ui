#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.template import defaultfilters as filters
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tables

from openstack_dashboard import api
from openstack_dashboard.dashboards.admin.aggregates import constants

from synapsdashboard.projects import tabs


class TenantFilterAction(tables.FilterAction):
    def filter(self, table, tenants, filter_string):
        """Really naive case-insensitive search."""
        # FIXME(gabriel): This should be smarter. Written for demo purposes.
        q = filter_string.lower()

        def comp(tenant):
            if q in tenant.name.lower():
                return True
            return False

        return filter(comp, tenants)
    

class MetricLink(tables.LinkAction):
    name = "metrics"
    verbose_name = _("View Metrics")
    url = "horizon:synapsdashboard:projects:monitoring"
    classes = ("btn-stats",)
    
    def get_link_url(self, datum):
        base_url = super(MetricLink, self).get_link_url(datum)
        tab_query_string = tabs.MetricsTab(
            tabs.MonitoringTabs, None).get_query_string()
        return "?".join([base_url, tab_query_string])
   

class AlarmLink(tables.LinkAction):
    name = "alarms"
    verbose_name = _("View Alarms")
    url = "horizon:synapsdashboard:projects:monitoring"
    classes = ("btn-stats",)
    
    def get_link_url(self, datum):
        base_url = super(AlarmLink, self).get_link_url(datum)
        tab_query_string = tabs.AlarmsTab(
            tabs.MonitoringTabs, None).get_query_string()
        return "?".join([base_url, tab_query_string])        

        
class TenantsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_('Name'),
                         form_field=forms.CharField(required=True,
                                                    max_length=64))
    description = tables.Column(lambda obj: getattr(obj, 'description', None),
                                verbose_name=_('Description'),
                                form_field=forms.CharField(
                                    widget=forms.Textarea(),
                                    required=False))
    id = tables.Column('id', verbose_name=_('Project ID'))
    enabled = tables.Column('enabled', verbose_name=_('Enabled'), status=True,
                            form_field=forms.BooleanField(
                                label=_('Enabled'),
                                required=False))

    class Meta:
        name = "tenants"
        verbose_name = _("Monitor Projects")
        row_actions = (AlarmLink, MetricLink)
        table_actions = (TenantFilterAction,)
        pagination_param = "tenant_marker"
        
