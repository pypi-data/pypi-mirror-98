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


class PortExports(object):
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
        'lun': 'str',
        'view': 'str',
        'volume': 'str',
        'status': 'str'
    }

    attribute_map = {
        'lun': 'lun',
        'view': 'view',
        'volume': 'volume',
        'status': 'status'
    }

    def __init__(self, lun=None, view=None, volume=None, status=None):  # noqa: E501
        """PortExports - a model defined in Swagger"""  # noqa: E501

        self._lun = None
        self._view = None
        self._volume = None
        self._status = None
        self.discriminator = None

        if lun is not None:
            self.lun = lun
        if view is not None:
            self.view = view
        if volume is not None:
            self.volume = volume
        if status is not None:
            self.status = status

    @property
    def lun(self):
        """Gets the lun of this PortExports.  # noqa: E501


        :return: The lun of this PortExports.  # noqa: E501
        :rtype: str
        """
        return self._lun

    @lun.setter
    def lun(self, lun):
        """Sets the lun of this PortExports.


        :param lun: The lun of this PortExports.  # noqa: E501
        :type: str
        """

        self._lun = lun

    @property
    def view(self):
        """Gets the view of this PortExports.  # noqa: E501


        :return: The view of this PortExports.  # noqa: E501
        :rtype: str
        """
        return self._view

    @view.setter
    def view(self, view):
        """Sets the view of this PortExports.


        :param view: The view of this PortExports.  # noqa: E501
        :type: str
        """

        self._view = view

    @property
    def volume(self):
        """Gets the volume of this PortExports.  # noqa: E501


        :return: The volume of this PortExports.  # noqa: E501
        :rtype: str
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this PortExports.


        :param volume: The volume of this PortExports.  # noqa: E501
        :type: str
        """

        self._volume = volume

    @property
    def status(self):
        """Gets the status of this PortExports.  # noqa: E501


        :return: The status of this PortExports.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this PortExports.


        :param status: The status of this PortExports.  # noqa: E501
        :type: str
        """

        self._status = status

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
        if issubclass(PortExports, dict):
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
        if not isinstance(other, PortExports):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
