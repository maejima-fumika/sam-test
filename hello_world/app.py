import json
import boto3
from . import Taskdb
from decimal import Decimal

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    endpoint_url = "http://localhost:8000"
    table_name = "Task"

    dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
    taskdb = Taskdb.Taskdb(dynamodb, table_name)

    try:
        method = event["body"]["method"]
        item = event["body"]["item"]
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
