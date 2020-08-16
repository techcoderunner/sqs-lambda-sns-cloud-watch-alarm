import json


def handler(event,context):
    print(f'Event Message: {json.dumps(event)}')

    c=1/0

    return {
        'statusCode': 200,
        'headers' : {
            'Content-Type' : "text/plain"
        },
        "body" : f'Hello CDK! The s3 object created succesfully!!!'
    }