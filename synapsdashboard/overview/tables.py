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

import logging

from horizon import tables
from horizon.utils import filters

class StatisticsTable(tables.DataTable):
    instance_name = tables.Column('name',
                                  link=("horizon:admin:instances:detail"))
    instance_id = tables.Column('instance_name', 
                                verbose_name="Instance ID")
    cpu_avg = tables.Column('cpu_avg', verbose_name="CPU Avg")
    cpu_min = tables.Column('cpu_min', verbose_name="CPU Min")
    cpu_max = tables.Column('cpu_max', verbose_name="CPU Max")
    
    netin_avg = tables.Column('netin_avg', verbose_name="Net In Avg")
    netin_min = tables.Column('netin_min', verbose_name="Net In Min")
    netin_max = tables.Column('netin_max', verbose_name="Net In Max")

    netout_avg = tables.Column('netout_avg', verbose_name="Net Out Avg")
    netout_min = tables.Column('netout_min', verbose_name="Net Out Min")
    netout_max = tables.Column('netout_max', verbose_name="Net Out Max")
    
    def get_object_id(self, datum):
        return datum.get("id")    
    
    class Meta:
        name = "statistics"
        verbose_name = _("Statistics")

class HistoryTable(tables.DataTable):
    timestamp = tables.Column('timestamp')
    name = tables.Column('name')
    tem_type = tables.Column('tem_type', verbose_name="Type")
    summary = tables.Column('summary')
    
    def get_object_id(self, datum):
        return datum.timestamp
    
    
    class Meta:
        name = "history"
        verbose_name = _("History")
#         table_actions = (MetricFilterAction, ViewMultiStatistics)
#         row_actions = (ViewGraph, CreateAlarm)
#         multi_select = True
#         pagination_param = "next_token"
