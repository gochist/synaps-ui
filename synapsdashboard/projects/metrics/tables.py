# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
#
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

from django.template.defaultfilters import title  # noqa
from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers

from horizon import tables

class MetricFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (('project', _("Project")),
                      ('name', _("Name"))
                      )
    needs_preloading = True

    def filter(self, table, metrics, filter_string):
        """Server side search.
        When filtering is supported in the api, then we will handle in view
        """
        return metrics



def pretty_dimensions(datum):
    dimensions = ["%s:%s" % (k, v[0]) for k, v in datum.dimensions.items()]
    return " ".join(dimensions)


class ViewMultiStatistics(tables.LinkAction):
    name = "multistatistics"
    verbose_name = _("Graph")
    url = "horizon:synapsdashboard:projects:graph"
    classes = ("ajax-modal", "btn-edit")
    
    
class CreateAlarm(tables.LinkAction):
    name = "createalarm"
    verbose_name = _("Create Alarm")
    url = "horizon:synapsdashboard:projects:graph"
    classes = ("ajax-modal", "btn-edit")
    

class ViewGraph(tables.LinkAction):
    name = "statistics"
    verbose_name = _("Graph")
    url = "horizon:synapsdashboard:projects:graph"
    classes = ("ajax-modal", "btn-edit")
    
    def get_link_url(self, datum=None):
        base_url = urlresolvers.reverse(self.url)        
        return base_url

#     def get_policy_target(self, request, datum=None):
#         project_id = None
#         if datum:
#             project_id = getattr(datum, 'tenant_id', None)
#         return {"project_id": project_id}
# 
#     def get_link_url(self, project):
#         return self._get_link_url(project, 'instance_info')
# 
#     def _get_link_url(self, project, step_slug):
#         base_url = urlresolvers.reverse(self.url, args=[project.id])
#         param = urlencode({"step": step_slug})
#         return "?".join([base_url, param])
# 
#     def allowed(self, request, instance):
#         return not is_deleting(instance)
        

class MetricsTable(tables.DataTable):
    namespace = tables.Column('namespace')
    metricname = tables.Column('name')
    dimensions = tables.Column(pretty_dimensions, verbose_name='Dimensions', 
                               wrap_list=True)
    
    class Meta:
        name = "metrics"
        verbose_name = _("Metrics")
        table_actions = (MetricFilterAction, ViewMultiStatistics)
        row_actions = (ViewGraph, CreateAlarm)
        multi_select = True
        pagination_param = "next_token"