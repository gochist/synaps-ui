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
from django.utils import http

import logging

from horizon import tables

class AlarmsFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (('project', _("Project")),
                      ('name', _("Name"))
                      )
    needs_preloading = True

    def filter(self, table, alarms, filter_string):
        return alarms


def pretty_dimensions(datum):
    dimensions = ["%s:%s" % (k, v[0]) for k, v in datum.dimensions.items()]
    return " ".join(dimensions)
    

class AlarmsTable(tables.DataTable):
    state_value = tables.Column('state_value', verbose_name='State')
    name = tables.Column('name', verbose_name='Alarm Name')
    namespace = tables.Column('namespace')
    metricname = tables.Column('metric', verbose_name='Metric Name')
    dimensions = tables.Column(pretty_dimensions, verbose_name='Dimensions',
                               wrap_list=True)
    state_reason = tables.Column('state_reason', verbose_name='Reason')


    def get_object_id(self, datum):
        return datum.name

    def get_marker(self):
        return http.urlquote_plus(self.data.next_token)
        
    class Meta:
        name = "alarms"
        verbose_name = _("Alarms")
        table_actions = (AlarmsFilterAction, )
        multi_select = True
        pagination_param = "next_token"
