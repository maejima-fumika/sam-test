import json
import boto3
from hello_world import Taskdb
from decimal import Decimal
import os


def lambda_handler(event, context):
    endpoint_url = os.environ["DYNAMODB_ENDPOINT"]
    table_name = os.environ["DYNAMODB_TABLE"]

    dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
    taskdb = Taskdb.Taskdb(dynamodb, table_name)

    body = json.loads(event["body"])

    try:
        method = body["method"]
        item = body["item"]
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": "required key does not exist"}),
        }

    statusCode, response = taskdb.execute_method(method, item)
    return {
        'statusCode': statusCode,
        'body': json.dumps(response, default=decimal_to_int),
    }


def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)
