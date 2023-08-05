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

from vplexapi.models.storage_array_family import StorageArrayFamily  # noqa: F401,E501


class MetaVolume(object):
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
        'active': 'bool',
        'application_consistent': 'bool',
        'block_count': 'int',
        'block_size': 'int',
        'capacity': 'int',
        'health_indications': 'list[str]',
        'health_state': 'str',
        'name': 'str',
        'operational_status': 'str',
        'storage_array_family': 'StorageArrayFamily',
        'system_id': 'str',
        'volume_uuid': 'str'
    }

    attribute_map = {
        'active': 'active',
        'application_consistent': 'application_consistent',
        'block_count': 'block_count',
        'block_size': 'block_size',
        'capacity': 'capacity',
        'health_indications': 'health_indications',
        'health_state': 'health_state',
        'name': 'name',
        'operational_status': 'operational_status',
        'storage_array_family': 'storage_array_family',
        'system_id': 'system_id',
        'volume_uuid': 'volume_uuid'
    }

    def __init__(self, active=None, application_consistent=None, block_count=None, block_size=None, capacity=None, health_indications=None, health_state=None, name=None, operational_status=None, storage_array_family=None, system_id=None, volume_uuid=None):  # noqa: E501
        """MetaVolume - a model defined in Swagger"""  # noqa: E501

        self._active = None
        self._application_consistent = None
        self._block_count = None
        self._block_size = None
        self._capacity = None
        self._health_indications = None
        self._health_state = None
        self._name = None
        self._operational_status = None
        self._storage_array_family = None
        self._system_id = None
        self._volume_uuid = None
        self.discriminator = None

        if active is not None:
            self.active = active
        if application_consistent is not None:
            self.application_consistent = application_consistent
        if block_count is not None:
            self.block_count = block_count
        if block_size is not None:
            self.block_size = block_size
        if capacity is not None:
            self.capacity = capacity
        if health_indications is not None:
            self.health_indications = health_indications
        if health_state is not None:
            self.health_state = health_state
        if name is not None:
            self.name = name
        if operational_status is not None:
            self.operational_status = operational_status
        if storage_array_family is not None:
            self.storage_array_family = storage_array_family
        if system_id is not None:
            self.system_id = system_id
        if volume_uuid is not None:
            self.volume_uuid = volume_uuid

    @property
    def active(self):
        """Gets the active of this MetaVolume.  # noqa: E501


        :return: The active of this MetaVolume.  # noqa: E501
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this MetaVolume.


        :param active: The active of this MetaVolume.  # noqa: E501
        :type: bool
        """

        self._active = active

    @property
    def application_consistent(self):
        """Gets the application_consistent of this MetaVolume.  # noqa: E501


        :return: The application_consistent of this MetaVolume.  # noqa: E501
        :rtype: bool
        """
        return self._application_consistent

    @application_consistent.setter
    def application_consistent(self, application_consistent):
        """Sets the application_consistent of this MetaVolume.


        :param application_consistent: The application_consistent of this MetaVolume.  # noqa: E501
        :type: bool
        """

        self._application_consistent = application_consistent

    @property
    def block_count(self):
        """Gets the block_count of this MetaVolume.  # noqa: E501


        :return: The block_count of this MetaVolume.  # noqa: E501
        :rtype: int
        """
        return self._block_count

    @block_count.setter
    def block_count(self, block_count):
        """Sets the block_count of this MetaVolume.


        :param block_count: The block_count of this MetaVolume.  # noqa: E501
        :type: int
        """

        self._block_count = block_count

    @property
    def block_size(self):
        """Gets the block_size of this MetaVolume.  # noqa: E501


        :return: The block_size of this MetaVolume.  # noqa: E501
        :rtype: int
        """
        return self._block_size

    @block_size.setter
    def block_size(self, block_size):
        """Sets the block_size of this MetaVolume.


        :param block_size: The block_size of this MetaVolume.  # noqa: E501
        :type: int
        """

        self._block_size = block_size

    @property
    def capacity(self):
        """Gets the capacity of this MetaVolume.  # noqa: E501


        :return: The capacity of this MetaVolume.  # noqa: E501
        :rtype: int
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this MetaVolume.


        :param capacity: The capacity of this MetaVolume.  # noqa: E501
        :type: int
        """

        self._capacity = capacity

    @property
    def health_indications(self):
        """Gets the health_indications of this MetaVolume.  # noqa: E501


        :return: The health_indications of this MetaVolume.  # noqa: E501
        :rtype: list[str]
        """
        return self._health_indications

    @health_indications.setter
    def health_indications(self, health_indications):
        """Sets the health_indications of this MetaVolume.


        :param health_indications: The health_indications of this MetaVolume.  # noqa: E501
        :type: list[str]
        """

        self._health_indications = health_indications

    @property
    def health_state(self):
        """Gets the health_state of this MetaVolume.  # noqa: E501


        :return: The health_state of this MetaVolume.  # noqa: E501
        :rtype: str
        """
        return self._health_state

    @health_state.setter
    def health_state(self, health_state):
        """Sets the health_state of this MetaVolume.


        :param health_state: The health_state of this MetaVolume.  # noqa: E501
        :type: str
        """

        self._health_state = health_state

    @property
    def name(self):
        """Gets the name of this MetaVolume.  # noqa: E501


        :return: The name of this MetaVolume.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MetaVolume.


        :param name: The name of this MetaVolume.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def operational_status(self):
        """Gets the operational_status of this MetaVolume.  # noqa: E501


        :return: The operational_status of this MetaVolume.  # noqa: E501
        :rtype: str
        """
        return self._operational_status

    @operational_status.setter
    def operational_status(self, operational_status):
        """Sets the operational_status of this MetaVolume.


        :param operational_status: The operational_status of this MetaVolume.  # noqa: E501
        :type: str
        """

        self._operational_status = operational_status

    @property
    def storage_array_family(self):
        """Gets the storage_array_family of this MetaVolume.  # noqa: E501


        :return: The storage_array_family of this MetaVolume.  # noqa: E501
        :rtype: StorageArrayFamily
        """
        return self._storage_array_family

    @storage_array_family.setter
    def storage_array_family(self, storage_array_family):
        """Sets the storage_array_family of this MetaVolume.


        :param storage_array_family: The storage_array_family of this MetaVolume.  # noqa: E501
        :type: StorageArrayFamily
        """

        self._storage_array_family = storage_array_family

    @property
    def system_id(self):
        """Gets the system_id of this MetaVolume.  # noqa: E501


        :return: The system_id of this MetaVolume.  # noqa: E501
        :rtype: str
        """
        return self._system_id

    @system_id.setter
    def system_id(self, system_id):
        """Sets the system_id of this MetaVolume.


        :param system_id: The system_id of this MetaVolume.  # noqa: E501
        :type: str
        """

        self._system_id = system_id

    @property
    def volume_uuid(self):
        """Gets the volume_uuid of this MetaVolume.  # noqa: E501


        :return: The volume_uuid of this MetaVolume.  # noqa: E501
        :rtype: str
        """
        return self._volume_uuid

    @volume_uuid.setter
    def volume_uuid(self, volume_uuid):
        """Sets the volume_uuid of this MetaVolume.


        :param volume_uuid: The volume_uuid of this MetaVolume.  # noqa: E501
        :type: str
        """

        self._volume_uuid = volume_uuid

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
        if issubclass(MetaVolume, dict):
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
        if not isinstance(other, MetaVolume):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
