import boto3

# Lists for testing
# regions = ["us-east-1","ap-southeast-1","ap-southeast-2","ap-northeast-1","eu-central-1","eu-west-1"]
# regions = ["eu-central-1"]

#Initialize argparser
parser = argparse.ArgumentParser(description='EC2 compliance check')
parser.add_argument("--h", help="--q to quit, --region AWS region")
parser.add_argument("--region", type=str, help="AWS region")
args = parser.parse_args()
regions = [args.region]

#AWS configuration for retry
config = Config(
    retries = dict(
        max_attempts = 10
    )
)

for region in regions:

   stack_session = boto3.client('cloudformation', config=config, region_name=region)
   
   paginator = stack_session.get_paginator('list_stacks')
   response_iterator = paginator.paginate()
   for page in response_iterator:
       stacks = page['StackSummaries']
       for stack in stacks:
         print(stack['StackName'])
         try:
             response = stack_session.detect_stack_drift(StackName = stack['StackName'])
             print(response)
         except:
             print("Drift detection failed")
