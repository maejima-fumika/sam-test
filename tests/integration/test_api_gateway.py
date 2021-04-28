import os
from unittest import TestCase
import json
import boto3
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""


class TestApiGateway(TestCase):
    api_endpoint: str

    @classmethod
    def get_stack_name(cls) -> str:
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")
        if not stack_name:
            return False

        return stack_name

    def setUp(self) -> None:
        """
        Based on the provided env variable AWS_SAM_STACK_NAME,
        here we use cloudformation API to find out what the HelloWorldApi URL is
        """
        stack_name = TestApiGateway.get_stack_name()

        if not stack_name:
            self.api_endpoint = os.environ.get("API_END_POINT")
            if not self.api_endpoint:
                raise Exception(
                    "Cannot find env var API_END_POINT. \n"
                    "Please setup this environment variable with api end point"
                )
            else:
                return

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name}. \n" f'Please make sure stack with the name "{stack_name}" exists.'
            ) from e

        stacks = response["Stacks"]

        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [
            output for output in stack_outputs if output["OutputKey"] == "HelloWorldApi"]
        self.assertTrue(
            api_outputs, f"Cannot find output HelloWorldApi in stack {stack_name}")

        self.api_endpoint = api_outputs[0]["OutputValue"]

    async def test_insert_dynamodb1(self):
        request_body = json.dumps(
            {"method": "insert", "item": {"Id": "1", "Name": "Task1"}})
        response = await requests.post(self.api_endpoint, request_body)
        assert response.status_code == 200

    async def test_get_dynamodb1(self):
        request_body = json.dumps(
            {"method": "insert", "item": {"Id": "1", "Name": ""}})
        response = await requests.post(self.api_endpoint, request_body)
        data = response.json()
        assert response.status_code == 200
        assert data["Id"] == 1
        assert data["Name"] == "Task1"

    async def test_update_dynamodb1(self):
        request_body = json.dumps(
            {"method": "update", "item": {"Id": "1", "Name": "Task1-2"}})
        response = await requests.post(self.api_endpoint, request_body)
        assert response.status_code == 200

    async def test_get_dynamodb2(self):
        request_body = json.dumps(
            {"method": "get", "item": {"Id": "1", "Name": ""}})
        response = await requests.post(self.api_endpoint, request_body)
        data = response.json()
        assert response.status_code == 200
        assert data["Id"] == 1
        assert data["Name"] == "Task1-2"

    async def test_insert_dynamodb2(self):
        request_body = json.dumps(
            {"method": "insert", "item": {"Id": "2", "Name": "Task2"}})
        response = await requests.post(self.api_endpoint, request_body)
        assert response.status_code == 200

    async def test_scan_dynamodb1(self):
        request_body = json.dumps(
            {"method": "scan", "item": {"Id": "", "Name": ""}})
        response = await requests.post(self.api_endpoint, request_body)
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 2

    async def test_delete_dynamodb1(self):
        request_body = json.dumps(
            {"method": "delete", "item": {"Id": "1", "Name": ""}})
        response = await requests.post(self.api_endpoint, request_body)
        assert response.status_code == 200

    async def test_delete_dynamodb2(self):
        request_body = json.dumps(
            {"method": "delete", "item": {"Id": "2", "Name": ""}})
        response = await requests.post(self.api_endpoint, request_body)
        assert response.status_code == 200

    async def test_scan_dynamodb2(self):
        request_body = json.dumps(
            {"method": "scan", "item": {"Id": "", "Name": ""}})
        response = await requests.post(self.api_endpoint, request_body)
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 0
