from __future__ import print_function

import json
import urllib
import boto3
import csv

print('Processes data and sends to DynamoDB tables')
print('Loading function')

customerTableName = 'Customer'
transactionsTableName = 'Transactions'

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
customerTable = dynamodb.Table(customerTableName);
transactionsTable = dynamodb.Table(transactionsTableName);

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the bucket and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    trnFileName = '/tmp/transactions.txt'
    try:
        s3.meta.client.download_file(bucket, key, trnFileName)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    # Read the Transactions CSV file. Delimiter is the '|' character
    with open(trnFileName) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            print(row['customer_id'], row['customer_address'], row['trn_id'], row['trn_date'], row['trn_amount'])
            # Insert customer id and address in customer DynamoDB table
            try:
                resp = customerTable.put_item(
                    Item={
                        'CustomerId': row['customer_id'],
                        'Address': row['customer_address']})
                resp = transactionsTable.put_item(
                    Item={
                        'CustomerId': row['customer_id'],
                        'TransactionId': row['trn_id'],
                        'TransactionDate': row['trn_date'],
                        'TransactionAmount': int(row['trn_amount'])})
            except Exception as e:
                 print(e)
                 print("Unable to insert data into DynamoDB table".format(e))

    return "done"
