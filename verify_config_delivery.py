from __future__ import print_function
import boto3
import re
import os
import sys
import getopt

n = "eu-west-1"     
result = True
failReason = ""
offenders = []
configClient = boto3.client('config', region_name=n)
response = configClient.describe_configuration_recorder_status()
# Get recording status
try:
    if not response['ConfigurationRecordersStatus'][0]['recording'] is True:
        result = False
        failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
        offenders.append(str(n) + ":NotRecording")
except:
    result = False
    failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
    offenders.append(str(n) + ":NotRecording")

# Verify that each region is capturing all events
response = configClient.describe_configuration_recorders()
try:
    if not response['ConfigurationRecorders'][0]['recordingGroup']['allSupported'] is True:
        result = False
        failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
        offenders.append(str(n) + ":NotAllEvents")
except:
    pass  # This indicates that Config is disabled in the region and will be captured above.

# Check if region is capturing global events. Fail is verified later since only one region needs to capture them.
try:
    if response['ConfigurationRecorders'][0]['recordingGroup']['includeGlobalResourceTypes'] is True:
        globalConfigCapture = True
except:
    pass

# Verify the delivery channels
response = configClient.describe_delivery_channel_status()
try:
    if response['DeliveryChannelsStatus'][0]['configHistoryDeliveryInfo']['lastStatus'] != "SUCCESS":
        result = False
        failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
        offenders.append(str(n) + ":S3Delivery")        
except:
    pass  # Will be captured by earlier rule
try:
    if response['DeliveryChannelsStatus'][0]['configStreamDeliveryInfo']['lastStatus'] != "SUCCESS":
        result = False
        failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
        offenders.append(str(n) + ":SNSDelivery")
except:
    pass  # Will be captured by earlier rule

print (offenders)