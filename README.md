# aws-cis-foundation-framework
Cloudformation template and compliance check python script. Modified AWS Provided Template and Checks.

Added SAM template for creating Lambda Function and Config Rule to schedule run every 24hour (default). Modify the template to run the compliance check according to your schedule. 

Valid Config Rule Schedules are One_Hour, Three_Hours, Six_Hours, Twelve_Hours, or TwentyFour_Hours

Create LambdaExuction Role and KMS Key and provide the arn when creating lambda function below.

## Execution Steps

1.Create Cloudwatch Metric Filters and Alarms 

aws cloudformation create-stack --stack-name cloudWatch-alarms-for-cloudtrail --template-body file://CloudWatch_Alarms_for_CloudTrail_API_Activity.json


2.Create Lambda Function and Cloudwatch Event Rule


aws cloudformation package --template-file serverless_stack.yaml --output-template-file serverless_stack_deploy.yaml --s3-bucket *yourbucketname*

aws cloudformation deploy --template-file serverless_stack_deploy.yaml --stack-name cis-compliance-check --parameter-overrides  LambdaExecutionRole=*RoleArn* KMSKey=*KeyArn*


3.Invoke Lambda Function (optional)

Invoke the following command to invoke lambda function to test the functionality. To test from AWS Config Click on Re-evaluate on the rule created

aws lambda invoke --function-name **function_name_created_above** *output_filename*


### References

1. [AWS Security Benchmark](https://github.com/awslabs/aws-security-benchmark/)
2. [Clodwatch Event Filter & Alarm](http://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html)
2. [Config Rule EventSource Details](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source-sourcedetails.html)