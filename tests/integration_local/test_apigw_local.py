import os
from unittest import TestCase

import boto3
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test.
"""

   def test_api_gateway(self):
        """
        Call the API Gateway endpoint and check the response
        """
        response = requests.get(self.api_endpoint)
        self.assertDictEqual(response.json(), {"message": "hello world"})

    def test_pytest(self):
        assert 1+2 == 3
