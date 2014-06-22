from horizon import views
import logging

from horizon import exceptions
from horizon import tables
from openstack_dashboard import api
from synapsdashboard.api import synaps
from synapsdashboard.alarms.tables import AlarmsTable


class AlarmCreateView(views.APIView):
    template_name = 'synapsdashboard/alarms/create.html'
    
    def get_context_data(self, **kwargs):
        return views.APIView.get_context_data(self, **kwargs)


class IndexView(tables.DataTableView):
    table_class = AlarmsTable 
    template_name = 'synapsdashboard/alarms/index.html'
    
#     # A very simple class-based view...

#     def get_alarms_data(self):
#         cw = synaps.get_cw_client(self.request)
#         alarms = cw.describe_alarms()
#         
#         return alarms

    def get_data(self):
        cw = synaps.get_cw_client(self.request)
        alarms = cw.describe_alarms()
        return alarms
    
