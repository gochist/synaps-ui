from horizon import views
import logging

from horizon import exceptions
from horizon import tables
from openstack_dashboard import api
from synapsdashboard.api import synaps
from synapsdashboard.metrics.tables import MetricsTable

class IndexView(tables.DataTableView):
    table_class = MetricsTable 
    template_name = 'synapsdashboard/metrics/index.html'


    def get_data(self):
        cw = synaps.get_cw_client(self.request)
        metrics = cw.list_metrics()
        return metrics
