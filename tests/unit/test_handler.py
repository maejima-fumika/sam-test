import json

import pytest

from hello_world import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    def _event(method, body):
        return {
            "body": {"method": method, "item": body},
            "resource": "/{proxy+}",
            "requestContext": {
                "resourceId": "123456",
                "apiId": "1234567890",
                "resourcePath": "/{proxy+}",
                "httpMethod": "POST",
                "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
                "accountId": "123456789012",
                "identity": {
                    "apiKey": "",
                    "userArn": "",
                    "cognitoAuthenticationType": "",
                    "caller": "",
                    "userAgent": "Custom User Agent String",
                    "user": "",
                    "cognitoIdentityPoolId": "",
                    "cognitoIdentityId": "",
                    "cognitoAuthenticationProvider": "",
                    "sourceIp": "127.0.0.1",
                    "accountId": "",
                },
                "stage": "prod",
            },
            "queryStringParameters": {"foo": "bar"},
            "headers": {
                "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
                "Accept-Language": "en-US,en;q=0.8",
                "CloudFront-Is-Desktop-Viewer": "true",
                "CloudFront-Is-SmartTV-Viewer": "false",
                "CloudFront-Is-Mobile-Viewer": "false",
                "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
                "CloudFront-Viewer-Country": "US",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Upgrade-Insecure-Requests": "1",
                "X-Forwarded-Port": "443",
                "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
                "X-Forwarded-Proto": "https",
                "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
                "CloudFront-Is-Tablet-Viewer": "false",
                "Cache-Control": "max-age=0",
                "User-Agent": "Custom User Agent String",
                "CloudFront-Forwarded-Proto": "https",
                "Accept-Encoding": "gzip, deflate, sdch",
            },
            "pathParameters": {"proxy": "/examplepath"},
            "httpMethod": "POST",
            "stageVariables": {"baz": "qux"},
            "path": "/examplepath",
        }

    return _event


# def test_lambda_handler(apigw_event, mocker):

#     ret = app.lambda_handler(apigw_event, "")
#     data = json.loads(ret["body"])

    # assert ret["statusCode"] == 200
    # assert "message" in ret["body"]
    # assert data["message"] == "hello world"
    # assert "location" in data.dict_keys()

def test_insert_dynamodb1(apigw_event, mocker):
    method = "insert"
    body = {"Id": "1", "Name": "Task1"}
    ret = app.lambda_handler(apigw_event(method, body), "")
    assert ret["statusCode"] == 200


def test_get_dynamodb1(apigw_event, mocker):
    method = "get"
    body = {"Id": "1", "Name": ""}
    ret = app.lambda_handler(apigw_event(method, body), "")
    data = json.loads(ret["body"])
    assert ret["statusCode"] == 200
    assert data["Id"] == 1
    assert data["Name"] == "Task1"


def test_update_dynamodb1(apigw_event, mocker):
    method = "update"
    body = {"Id": "1", "Name": "Task1-2"}
    ret = app.lambda_handler(apigw_event(method, body), "")
    data = json.loads(ret["body"])
    print(data)
    assert ret["statusCode"] == 200


def test_get_dynamodb2(apigw_event, mocker):
    method = "get"
    body = {"Id": "1", "Name": ""}
    ret = app.lambda_handler(apigw_event(method, body), "")
    data = json.loads(ret["body"])
    assert ret["statusCode"] == 200
    assert data["Id"] == 1
    assert data["Name"] == "Task1-2"


def test_insert_dynamodb2(apigw_event, mocker):
    method = "insert"
    body = {"Id": "2", "Name": "Task2"}
    ret = app.lambda_handler(apigw_event(method, body), "")
    assert ret["statusCode"] == 200


def test_scan_dynamodb1(apigw_event, mocker):
    method = "scan"
    body = {"Id": "-1", "Name": ""}
    ret = app.lambda_handler(apigw_event(method, body), "")
    data = json.loads(ret["body"])
    print(data)
    assert ret["statusCode"] == 200
    assert len(data) == 2


def test_delete_dynamodb1(apigw_event, mocker):
    method = "delete"
    body = {"Id": "1", "Name": ""}
    ret = app.lambda_handler(apigw_event(method, body), "")
    assert ret["statusCode"] == 200


def test_delete_dynamodb2(apigw_event, mocker):
    method = "delete"
    body = {"Id": "2", "Name": ""}
    ret = app.lambda_handler(apigw_event(method, body), "")
    assert ret["statusCode"] == 200


def test_scan_dynamodb2(apigw_event, mocker):
    method = "scan"
    body = {"Id": "-1", "Name": ""}
    ret = app.lambda_handler(apigw_event(method, body), "")
    data = json.loads(ret["body"])
    print(data)
    assert ret["statusCode"] == 200
    assert len(data) == 0
