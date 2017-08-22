# aws-cis-foundation-framework
Cloudformation template and compliance check python script. Modified AWS Provided Template and Checks -

[AWS Security Benchmark](https://github.com/awslabs/aws-security-benchmark/)

Added SAM template for creating Lambda Function and Cloudwatch Event Rule to schedule run every hour

## Execution Steps

1. Create Cloudwatch Metric Filters and Alarms 
aws cloudformation create-stack --stack-name cloudWatch-alarms-for-cloudtrail --template-body file://CloudWatch_Alarms_for_CloudTrail_API_Activity.json

2. Create Lambda Function and Cloudwatch Event Rule
aws cloudformation package --template-file serverless_stack.yaml --output-template-file serverless_stack_deploy.yaml --s3-bucket *yourbucketname*
aws cloudformation deploy --template-file serverless_stack_deploy.yaml --stack-name cis-compliance-check --parameter-overrides  LambdaExecutionRole=*RoleArn* KMSKey=*KeyArn*

3. Invoke Lambda Function
aws lambda invoke --function-name **function_name_created_above** *output_filename*

### References
1. [Clodwatch Event Filter & Alarm](http://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html)