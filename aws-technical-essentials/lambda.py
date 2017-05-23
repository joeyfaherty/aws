from __future__ import print_function

import json
import boto3

print('Loading function')


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    # Extract the EC2 instance id from the Auto Scaling lifecycle event notification
    message = event['Records'][0]['Sns']['Message']
    autoscalingInfo = json.loads(message)
    ec2InstanceId = autoscalingInfo['EC2InstanceId']

    print ("***Adding tag to EC2 instance with id: " + ec2InstanceId)

    # Add a tag to the EC2 instance: Key = ManualScaling, Value = Yes
    ec2 = boto3.client('ec2')
    response = ec2.create_tags(
        DryRun=False,
        Resources=[
            ec2InstanceId
        ],
        Tags=[
            {
                'Key': 'ManualScaling',
                'Value': 'Yes'
            },
        ]
    )

    ec2 = boto3.resource('ec2')

    print ("***Creating snapshot of volumes attached to EC2 instance with id: " + ec2InstanceId)

    for v in ec2.volumes.filter(Filters=[{'Name': 'attachment.instance-id', 'Values': [ec2InstanceId]}]):
        print(v.volume_id)
        description = 'autosnap-%s-%s' % ( ec2InstanceId, v.volume_id )

        if v.create_snapshot(description):
            print("\t\tSnapshot created with description [%s]" % description)

    return "ec2InstanceId"
