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

from vplexapi.models.connectivity_status import ConnectivityStatus  # noqa: F401,E501
from vplexapi.models.storage_array_family import StorageArrayFamily  # noqa: F401,E501


class StorageArray(object):
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
        'name': 'str',
        'controllers': 'list[str]',
        'auto_switch': 'bool',
        'connectivity_status': 'ConnectivityStatus',
        'ports': 'list[str]',
        'logical_unit_count': 'int',
        'product_revision': 'str',
        'storage_array_family': 'StorageArrayFamily',
        'storage_pools': 'str',
        'storage_groups': 'str'
    }

    attribute_map = {
        'name': 'name',
        'controllers': 'controllers',
        'auto_switch': 'auto_switch',
        'connectivity_status': 'connectivity_status',
        'ports': 'ports',
        'logical_unit_count': 'logical_unit_count',
        'product_revision': 'product_revision',
        'storage_array_family': 'storage_array_family',
        'storage_pools': 'storage_pools',
        'storage_groups': 'storage_groups'
    }

    def __init__(self, name=None, controllers=None, auto_switch=None, connectivity_status=None, ports=None, logical_unit_count=None, product_revision=None, storage_array_family=None, storage_pools=None, storage_groups=None):  # noqa: E501
        """StorageArray - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._controllers = None
        self._auto_switch = None
        self._connectivity_status = None
        self._ports = None
        self._logical_unit_count = None
        self._product_revision = None
        self._storage_array_family = None
        self._storage_pools = None
        self._storage_groups = None
        self.discriminator = None

        self.name = name
        if controllers is not None:
            self.controllers = controllers
        if auto_switch is not None:
            self.auto_switch = auto_switch
        if connectivity_status is not None:
            self.connectivity_status = connectivity_status
        if ports is not None:
            self.ports = ports
        if logical_unit_count is not None:
            self.logical_unit_count = logical_unit_count
        if product_revision is not None:
            self.product_revision = product_revision
        if storage_array_family is not None:
            self.storage_array_family = storage_array_family
        if storage_pools is not None:
            self.storage_pools = storage_pools
        if storage_groups is not None:
            self.storage_groups = storage_groups

    @property
    def name(self):
        """Gets the name of this StorageArray.  # noqa: E501


        :return: The name of this StorageArray.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this StorageArray.


        :param name: The name of this StorageArray.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def controllers(self):
        """Gets the controllers of this StorageArray.  # noqa: E501


        :return: The controllers of this StorageArray.  # noqa: E501
        :rtype: list[str]
        """
        return self._controllers

    @controllers.setter
    def controllers(self, controllers):
        """Sets the controllers of this StorageArray.


        :param controllers: The controllers of this StorageArray.  # noqa: E501
        :type: list[str]
        """

        self._controllers = controllers

    @property
    def auto_switch(self):
        """Gets the auto_switch of this StorageArray.  # noqa: E501


        :return: The auto_switch of this StorageArray.  # noqa: E501
        :rtype: bool
        """
        return self._auto_switch

    @auto_switch.setter
    def auto_switch(self, auto_switch):
        """Sets the auto_switch of this StorageArray.


        :param auto_switch: The auto_switch of this StorageArray.  # noqa: E501
        :type: bool
        """

        self._auto_switch = auto_switch

    @property
    def connectivity_status(self):
        """Gets the connectivity_status of this StorageArray.  # noqa: E501


        :return: The connectivity_status of this StorageArray.  # noqa: E501
        :rtype: ConnectivityStatus
        """
        return self._connectivity_status

    @connectivity_status.setter
    def connectivity_status(self, connectivity_status):
        """Sets the connectivity_status of this StorageArray.


        :param connectivity_status: The connectivity_status of this StorageArray.  # noqa: E501
        :type: ConnectivityStatus
        """

        self._connectivity_status = connectivity_status

    @property
    def ports(self):
        """Gets the ports of this StorageArray.  # noqa: E501


        :return: The ports of this StorageArray.  # noqa: E501
        :rtype: list[str]
        """
        return self._ports

    @ports.setter
    def ports(self, ports):
        """Sets the ports of this StorageArray.


        :param ports: The ports of this StorageArray.  # noqa: E501
        :type: list[str]
        """

        self._ports = ports

    @property
    def logical_unit_count(self):
        """Gets the logical_unit_count of this StorageArray.  # noqa: E501


        :return: The logical_unit_count of this StorageArray.  # noqa: E501
        :rtype: int
        """
        return self._logical_unit_count

    @logical_unit_count.setter
    def logical_unit_count(self, logical_unit_count):
        """Sets the logical_unit_count of this StorageArray.


        :param logical_unit_count: The logical_unit_count of this StorageArray.  # noqa: E501
        :type: int
        """

        self._logical_unit_count = logical_unit_count

    @property
    def product_revision(self):
        """Gets the product_revision of this StorageArray.  # noqa: E501


        :return: The product_revision of this StorageArray.  # noqa: E501
        :rtype: str
        """
        return self._product_revision

    @product_revision.setter
    def product_revision(self, product_revision):
        """Sets the product_revision of this StorageArray.


        :param product_revision: The product_revision of this StorageArray.  # noqa: E501
        :type: str
        """

        self._product_revision = product_revision

    @property
    def storage_array_family(self):
        """Gets the storage_array_family of this StorageArray.  # noqa: E501


        :return: The storage_array_family of this StorageArray.  # noqa: E501
        :rtype: StorageArrayFamily
        """
        return self._storage_array_family

    @storage_array_family.setter
    def storage_array_family(self, storage_array_family):
        """Sets the storage_array_family of this StorageArray.


        :param storage_array_family: The storage_array_family of this StorageArray.  # noqa: E501
        :type: StorageArrayFamily
        """

        self._storage_array_family = storage_array_family

    @property
    def storage_pools(self):
        """Gets the storage_pools of this StorageArray.  # noqa: E501


        :return: The storage_pools of this StorageArray.  # noqa: E501
        :rtype: str
        """
        return self._storage_pools

    @storage_pools.setter
    def storage_pools(self, storage_pools):
        """Sets the storage_pools of this StorageArray.


        :param storage_pools: The storage_pools of this StorageArray.  # noqa: E501
        :type: str
        """

        self._storage_pools = storage_pools

    @property
    def storage_groups(self):
        """Gets the storage_groups of this StorageArray.  # noqa: E501


        :return: The storage_groups of this StorageArray.  # noqa: E501
        :rtype: str
        """
        return self._storage_groups

    @storage_groups.setter
    def storage_groups(self, storage_groups):
        """Sets the storage_groups of this StorageArray.


        :param storage_groups: The storage_groups of this StorageArray.  # noqa: E501
        :type: str
        """

        self._storage_groups = storage_groups

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
        if issubclass(StorageArray, dict):
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
        if not isinstance(other, StorageArray):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
