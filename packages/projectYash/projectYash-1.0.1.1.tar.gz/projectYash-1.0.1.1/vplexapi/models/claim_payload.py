# coding: utf-8

"""
    VPlex REST API

    A definition for the next-gen VPlex API  # noqa: E501

    OpenAPI spec version: 0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ClaimPayload(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'application_consistent': 'bool'
    }

    attribute_map = {
        'application_consistent': 'application_consistent'
    }

    def __init__(self, application_consistent=None):  # noqa: E501
        """ClaimPayload - a model defined in Swagger"""  # noqa: E501

        self._application_consistent = None
        self.discriminator = None

        if application_consistent is not None:
            self.application_consistent = application_consistent

    @property
    def application_consistent(self):
        """Gets the application_consistent of this ClaimPayload.  # noqa: E501

        Set to mark the volume as application consistent  # noqa: E501

        :return: The application_consistent of this ClaimPayload.  # noqa: E501
        :rtype: bool
        """
        return self._application_consistent

    @application_consistent.setter
    def application_consistent(self, application_consistent):
        """Sets the application_consistent of this ClaimPayload.

        Set to mark the volume as application consistent  # noqa: E501

        :param application_consistent: The application_consistent of this ClaimPayload.  # noqa: E501
        :type: bool
        """

        self._application_consistent = application_consistent

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ClaimPayload, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ClaimPayload):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
