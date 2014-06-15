import boto
import logging

synaps = boto.connect_cloudwatch()

list_metrics = synaps.list_metrics
describe_alarms = synaps.describe_alarms

def get_namespace_metricname_map(project_id):
    metrics = synaps.list_metrics(metric_name="MetricCount",
                                  dimensions={"namespace":[""],
                                              "metricName":[""]},
                                  project_id=project_id)
    
    ret = {}
    
    for m in metrics:
        namespace = m.dimensions["namespace"][0]
        metric_name = m.dimensions["metricName"][0] 
        if namespace in ret:
            ret[namespace].append(metric_name)
        else:
            ret[namespace] = [metric_name]
                    
    return ret
