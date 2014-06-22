from horizon import views
import logging

from horizon import exceptions
from horizon import tables
from openstack_dashboard import api
from synapsdashboard.api import synaps
from synapsdashboard.overview.tables import HistoryTable, StatisticsTable
from datetime import datetime, timedelta


class IndexView(tables.MultiTableView):
    table_classes = (HistoryTable, StatisticsTable) 
    template_name = 'synapsdashboard/overview/index.html'

    def get_statistics_data(self):
        cw = synaps.get_cw_client(self.request)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=24)

        servers, __ = api.nova.server_list(self.request,
                                           search_opts={"status": "active"})
        
        ret = []
        for s in servers:
            datum = {}
            datum["id"] = getattr(s, "id") 
            datum["name"] = getattr(s, "name") 
            datum["instance_name"] = getattr(s, "OS-EXT-SRV-ATTR:instance_name")
            cpu_stats = cw.get_metric_statistics(period=60 * 60 * 24,
                              start_time=end_date,
                              end_time=end_date,
                              metric_name="CPUUtilization",
                              namespace="SPCS/NOVA",
                              statistics=["Average", "Minimum", "Maximum"],
                              dimensions={"instanceId":
                                          datum["instance_name"]})
            netin_stats = cw.get_metric_statistics(period=60 * 60 * 24,
                              start_time=end_date,
                              end_time=end_date,
                              metric_name="NetworkIn",
                              namespace="SPCS/NOVA",
                              statistics=["Average", "Minimum", "Maximum"],
                              dimensions={"instanceId":
                                          datum["instance_name"]})
            netout_stats = cw.get_metric_statistics(period=60 * 60 * 24,
                              start_time=end_date,
                              end_time=end_date,
                              metric_name="NetworkOut",
                              namespace="SPCS/NOVA",
                              statistics=["Average", "Minimum", "Maximum"],
                              dimensions={"instanceId":
                                          datum["instance_name"]})            
            if cpu_stats:
                datum["cpu_avg"] = cpu_stats[-1]["Average"]
                datum["cpu_max"] = cpu_stats[-1]["Maximum"]
                datum["cpu_min"] = cpu_stats[-1]["Minimum"]

            if netin_stats:
                datum["netin_avg"] = netin_stats[-1]["Average"]
                datum["netin_max"] = netin_stats[-1]["Maximum"]
                datum["netin_min"] = netin_stats[-1]["Minimum"]

            if netout_stats:
                datum["netout_avg"] = netout_stats[-1]["Average"]
                datum["netout_max"] = netout_stats[-1]["Maximum"]
                datum["netout_min"] = netout_stats[-1]["Minimum"]
            
            ret.append(datum)
            
        return ret

    def get_history_data(self):
        cw = synaps.get_cw_client(self.request)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=24)
        history = cw.describe_alarm_history(start_date=start_date,
                                            end_date=end_date,
                                            max_records=20)
        history.sort(cmp=lambda x, y: cmp(x.timestamp, y.timestamp),
                     reverse=True)
        return history

