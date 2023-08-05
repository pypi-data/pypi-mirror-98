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


class RegisterPayload(object):
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
        'port_wwn': 'str',
        'iscsi_name': 'str',
        'port_name': 'str',
        'node_wwn': 'str',
        'type': 'str'
    }

    attribute_map = {
        'port_wwn': 'port_wwn',
        'iscsi_name': 'iscsi_name',
        'port_name': 'port_name',
        'node_wwn': 'node_wwn',
        'type': 'type'
    }

    def __init__(self, port_wwn=None, iscsi_name=None, port_name=None, node_wwn=None, type=None):  # noqa: E501
        """RegisterPayload - a model defined in Swagger"""  # noqa: E501

        self._port_wwn = None
        self._iscsi_name = None
        self._port_name = None
        self._node_wwn = None
        self._type = None
        self.discriminator = None

        if port_wwn is not None:
            self.port_wwn = port_wwn
        if iscsi_name is not None:
            self.iscsi_name = iscsi_name
        self.port_name = port_name
        if node_wwn is not None:
            self.node_wwn = node_wwn
        if type is not None:
            self.type = type

    @property
    def port_wwn(self):
        """Gets the port_wwn of this RegisterPayload.  # noqa: E501

        WWN of the port to register. Either port_wwn or iscsi_name should be provided.  # noqa: E501

        :return: The port_wwn of this RegisterPayload.  # noqa: E501
        :rtype: str
        """
        return self._port_wwn

    @port_wwn.setter
    def port_wwn(self, port_wwn):
        """Sets the port_wwn of this RegisterPayload.

        WWN of the port to register. Either port_wwn or iscsi_name should be provided.  # noqa: E501

        :param port_wwn: The port_wwn of this RegisterPayload.  # noqa: E501
        :type: str
        """

        self._port_wwn = port_wwn

    @property
    def iscsi_name(self):
        """Gets the iscsi_name of this RegisterPayload.  # noqa: E501

        ISCSI name of the port to register. Either port_wwn or iscsi_name should be provided.  # noqa: E501

        :return: The iscsi_name of this RegisterPayload.  # noqa: E501
        :rtype: str
        """
        return self._iscsi_name

    @iscsi_name.setter
    def iscsi_name(self, iscsi_name):
        """Sets the iscsi_name of this RegisterPayload.

        ISCSI name of the port to register. Either port_wwn or iscsi_name should be provided.  # noqa: E501

        :param iscsi_name: The iscsi_name of this RegisterPayload.  # noqa: E501
        :type: str
        """

        self._iscsi_name = iscsi_name

    @property
    def port_name(self):
        """Gets the port_name of this RegisterPayload.  # noqa: E501

        Provide a new name for the registered initiator port.  # noqa: E501

        :return: The port_name of this RegisterPayload.  # noqa: E501
        :rtype: str
        """
        return self._port_name

    @port_name.setter
    def port_name(self, port_name):
        """Sets the port_name of this RegisterPayload.

        Provide a new name for the registered initiator port.  # noqa: E501

        :param port_name: The port_name of this RegisterPayload.  # noqa: E501
        :type: str
        """
        if port_name is None:
            raise ValueError("Invalid value for `port_name`, must not be `None`")  # noqa: E501

        self._port_name = port_name

    @property
    def node_wwn(self):
        """Gets the node_wwn of this RegisterPayload.  # noqa: E501

        Provide node wwn for registering the port.  # noqa: E501

        :return: The node_wwn of this RegisterPayload.  # noqa: E501
        :rtype: str
        """
        return self._node_wwn

    @node_wwn.setter
    def node_wwn(self, node_wwn):
        """Sets the node_wwn of this RegisterPayload.

        Provide node wwn for registering the port.  # noqa: E501

        :param node_wwn: The node_wwn of this RegisterPayload.  # noqa: E501
        :type: str
        """

        self._node_wwn = node_wwn

    @property
    def type(self):
        """Gets the type of this RegisterPayload.  # noqa: E501

        Provide host type for registering the port.  # noqa: E501

        :return: The type of this RegisterPayload.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this RegisterPayload.

        Provide host type for registering the port.  # noqa: E501

        :param type: The type of this RegisterPayload.  # noqa: E501
        :type: str
        """

        self._type = type

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
        if issubclass(RegisterPayload, dict):
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
        if not isinstance(other, RegisterPayload):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
