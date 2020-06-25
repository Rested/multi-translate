# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import multitranslateclient
from multitranslateclient.models.validation_error import ValidationError  # noqa: E501
from multitranslateclient.rest import ApiException

class TestValidationError(unittest.TestCase):
    """ValidationError unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ValidationError
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = multitranslateclient.models.validation_error.ValidationError()  # noqa: E501
        if include_optional :
            return ValidationError(
                loc = [
                    '0'
                    ], 
                msg = '0', 
                type = '0'
            )
        else :
            return ValidationError(
                loc = [
                    '0'
                    ],
                msg = '0',
                type = '0',
        )

    def testValidationError(self):
        """Test ValidationError"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
