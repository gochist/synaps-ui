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

    def has_more_data(self, table):
        return self._more
    
    def get_data(self):
        cw = synaps.get_cw_client(self.request)
        marker = self.request.GET.get(MetricsTable._meta.pagination_param, 
                                      None)
        
        metrics = cw.list_metrics(next_token=marker)
        self._more = metrics.next_token
        
        return metrics
