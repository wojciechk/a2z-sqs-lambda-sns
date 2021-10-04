import json
import boto3
import os

FLAGGED_WORDS=['oracle', 'acme', 'azure','foo', 'bar']

OUPUT_TOPIC_ARN=os.getenv('OUPUT_TOPIC_ARN')

SNS = boto3.client ('sns', region_name='us-east-1')

def lambda_handler(event, context):
    print("event: "+json.dumps(event))

    records=event['Records']
    print(records)
    for record in records:
        print(record)
        event=json.loads(record['body'])
        soup="".join(str(v) for k,v in event['textFields'].items()).lower()
        matches =  { match for match in FLAGGED_WORDS if match in soup.lower() }
        print(str(matches)+' for: '+soup)
        if len(matches)>0:
            payload=json.dumps({
                'productID': event['productID'],
                'matches': list(matches)
            })
            print("there are matches, sending payload "+ payload)
            response = {
                'statusCode': 200,
                'body': payload
            }
            SNS.publish(TopicArn=OUPUT_TOPIC_ARN, Message=payload, Subject='Match !')
    return {
        'statusCode': 404
    }
