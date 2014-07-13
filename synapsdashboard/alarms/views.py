from horizon import views
import logging

from horizon import exceptions
from horizon import tables
from openstack_dashboard import api
from synapsdashboard.api import synaps
from synapsdashboard.alarms.tables import AlarmsTable
from horizon.utils import functions as utils


class AlarmCreateView(views.APIView):
    template_name = 'synapsdashboard/alarms/create.html'
    
    def get_context_data(self, metric, **kwargs):
        return views.APIView.get_context_data(self, **kwargs)


class IndexView(tables.DataTableView):
    table_class = AlarmsTable 
    template_name = 'synapsdashboard/alarms/index.html'

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        cw = synaps.get_cw_client(self.request)

        marker = self.request.GET.get(AlarmsTable._meta.pagination_param, None)
        state_value = self.request.GET.get("state_value", None)
        alarm_name_prefix = self.request.GET.get("alarm_name_prefix", None)
        size = utils.get_page_size(self.request, 20)
        
        alarms = cw.describe_alarms(max_records=size, next_token=marker,
                                    state_value=state_value, 
                                    alarm_name_prefix=alarm_name_prefix)
        
        self._more = alarms.next_token
        return alarms
    
