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

from django import template
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

import logging
import json

from openstack_dashboard import api

from synapsdashboard.api import synaps
from synapsdashboard.projects.metrics.tables import MetricsTable
from synapsdashboard.projects.alarms.tables import AlarmsTable    

class MetricsTab(tabs.TableTab):
    table_classes = (MetricsTable,)
    name = _("Metrics")
    slug = "metrics"
    template_name = ("synapsdashboard/projects/"
                     "_monitoring_metrics.html")
    
    def _get_tenant_id(self):
        return self.tab_group.kwargs['tenant_id']
    
    def get_context_data(self, request):
        tenant_id = self._get_tenant_id()
        context = tabs.TableTab.get_context_data(self, request)
        ns_name_map = synaps.get_namespace_metricname_map(project_id=tenant_id)
        context['ns_name_map'] = ns_name_map
        return context
    
    def get_metrics_data(self):
        tenant_id = self._get_tenant_id()
        metrics = synaps.list_metrics(project_id=tenant_id)
        ret = []
        for n, m in enumerate(metrics):
            logging.info(dir(m))
            m.id = n
            m.tenant_id = tenant_id
            ret.append(m) 
        return ret
    
    
class AlarmsTab(tabs.TableTab):
    table_classes = (AlarmsTable,)
    name = _("Alarms")
    slug = "alarms"
    template_name = ("synapsdashboard/projects/"
                     "_monitoring_alarms.html")

    def _get_tenant_id(self):
        return self.tab_group.kwargs['tenant_id']
    
    def get_context_data(self, request):
        context = tabs.TableTab.get_context_data(self, request)
        return context
    
    def get_alarms_data(self):
        tenant_id = self._get_tenant_id()
        alarms = synaps.describe_alarms(project_id=tenant_id)
        
        ret = []
        for n, a in enumerate(alarms):
            logging.info(dir(a))
            a.id = n
            ret.append(a)
        return ret
    
class MonitoringTabs(tabs.TabGroup):
    slug = "synapsadmin"
    tabs = (AlarmsTab, MetricsTab)
#     sticky = True
    kwargs = {}
