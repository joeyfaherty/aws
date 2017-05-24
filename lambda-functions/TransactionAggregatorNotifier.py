from __future__ import print_function

import json
import boto3

print('Updates transaction totals; sends notifications for balance exceeding 1500')
print('Loading function')

### STUDENT TODO: Update the value of snsTopicArn ###
snsTopicArn = '<ARN for HighAccountBalanceAlertSNSTopic>'

dynamodb = boto3.resource('dynamodb')
transactionTotalTableName = 'TransactionTotal'
transactionsTotalTable = dynamodb.Table(transactionTotalTableName);

sns = boto3.client('sns')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:
        customerId = record['dynamodb']['NewImage']['CustomerId']['S']
        transactionAmount = int(record['dynamodb']['NewImage']['TransactionAmount']['N'])

        response = transactionsTotalTable.update_item(
            Key={
                'CustomerId': customerId
            },
            UpdateExpression="add accountBalance :val",
            ExpressionAttributeValues={
                ':val': transactionAmount
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Added transaction to account balance in TransactionTotal table")

        latestAccountBalance = response['Attributes']['accountBalance']
        print("Latest account balance: ".format(latestAccountBalance))

        if latestAccountBalance  >= 1500:
            message = '{"customerID": "' + customerId + '", ' + '"accountBalance": "' + str(latestAccountBalance) + '"}'
            print(message)
            print("Account balance is very high: ".format(latestAccountBalance))
            sns.publish(
                TopicArn=snsTopicArn,
                Message=message,
                Subject='Warning! Account balance is very high',
                MessageStructure='raw'
            )


    return 'Successfully processed {} records.'.format(len(event['Records']))
