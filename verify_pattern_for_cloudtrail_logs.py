from __future__ import print_function
import boto3
import re
import os
import sys
import getopt

def find_in_string(pattern, target):
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    for n in pattern:
        if not re.search(n, target):
            result = False
            print ("{0} not found".format(n))
            break
    return result

m = "ap-southeast-2"
group = "logs-cloudtrail"
client = boto3.client('logs', region_name=m)
filters = client.describe_metric_filters(logGroupName=group)
for p in filters['metricFilters']:
  # print (str(p['filterPattern']))
  patterns = ["\$\.eventName\s*=\s*\"?ConsoleLogin(\"|\)|\s)", "\$\.additionalEventData\.MFAUsed\s*\!=\s*\"?Yes|\s"]  
  # patterns = ["\$\.errorCode\s*=\s*\"?\*UnauthorizedOperation(\"|\)|\s)", "\$\.errorCode\s*=\s*\"?AccessDenied\*(\"|\)|\s)"]
  if find_in_string(patterns, str(p['filterPattern'])):
    cwclient = boto3.client('cloudwatch', region_name=m)
    response = cwclient.describe_alarms_for_metric(
      MetricName=p['metricTransformations'][0]['metricName'],
      Namespace=p['metricTransformations'][0]['metricNamespace']
      )
    print (response)